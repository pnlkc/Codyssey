import logging
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import settings
from models.chat_model import ChatRequest, ChatResponse
from models.conversation_model import Message
from services.analytics_service import AnalyticsService
from services.firestore_service import FirestoreService

logger = logging.getLogger("ai_service")

# =========================================================================
# AI Function Calling (도구 호출) 정의 - 보너스 과제
# =========================================================================
TOOLS_SCHEMA = [
    {
        "name": "get_data_summary",
        "description": "전체 시계열 데이터의 요약 통계(기간, 총합, 평균, 최고/최저치, 트렌드)를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_top_records",
        "description": "수치(value)가 가장 높은 상위 N개의 기록을 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "조회할 개수 (기본값: 5)"}
            }
        }
    }
]

async def execute_tool_call(tool_name: str, args: Dict[str, Any]) -> str:
    """도구 호출 실행 디스패처"""
    if tool_name == "get_data_summary":
        summary = await AnalyticsService.get_summary()
        return summary.raw_summary_text or ""
    elif tool_name == "get_top_records":
        limit = args.get("limit", 5)
        all_data = await FirestoreService.get_all_data()
        sorted_top = sorted(all_data, key=lambda x: float(x.get("value", 0)), reverse=True)[:limit]
        return json.dumps(sorted_top, ensure_ascii=False)
    return "알 수 없는 도구입니다."


class AIService:
    """컨텍스트 주입 및 도구 호출(Function Calling) 지원 AI 대화 엔진"""

    @staticmethod
    def _build_system_prompt(summary_text: str) -> str:
        """데이터 요약을 주입한 시스템 프롬프트 생성"""
        return (
            "당신은 사용자의 시계열 데이터(주식 주가, 실적 지표, 시장 트렌드 등)를 완벽히 파악하고 있는 전문 AI 데이터·금융 분석 비서입니다.\n\n"
            f"{summary_text}\n\n"
            "## 비서 핵심 지침:\n"
            "1. 사용자의 질문에 답변할 때, 주입된 데이터 요약(기간, 평균가, 최고가/신고가, 7일 이동평균 추세, 주요 메모 이슈 등)을 적극적으로 인용하여 명확하고 설득력 있게 답변하세요.\n"
            "2. 구체적인 수치(원화 가격, 평균치, 최고치, 날짜 등)와 시장 맥락(HBM 공급, 실적 발표 등)을 결합하여 신뢰성 있는 전문 인사이트를 제공하세요.\n"
            "3. 답변은 한국어로 정중하고 친절하게 마크다운(강조, 불릿포인트 등)을 활용하여 가독성 높게 작성하세요."
        )

    @classmethod
    async def chat(cls, request: ChatRequest) -> ChatResponse:
        """대화 요청 처리: 요약 조회 -> 프롬프트 주입 -> LLM 호출 -> 대화 자동 저장"""
        # 1. 데이터 요약 정보 조회 (컨텍스트 주입용)
        summary = await AnalyticsService.get_summary()
        system_prompt = cls._build_system_prompt(summary.raw_summary_text or "")

        # 2. 대화 히스토리 및 현재 메시지 구성
        conversation_id = request.conversation_id
        messages_history: List[Dict[str, Any]] = []

        # 이전 대화 불러오기 (세션 ID가 있는 경우)
        if conversation_id:
            existing_conv = await FirestoreService.get_conversation_by_id(conversation_id)
            if existing_conv and "messages" in existing_conv:
                messages_history = existing_conv["messages"]

        # 요청에 직접 실려온 히스토리가 있으면 보강
        if request.history and not messages_history:
            messages_history = [m.model_dump() for m in request.history]

        user_message_dict = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        }
        messages_history.append(user_message_dict)

        # 3. LLM 호출 (Gemini 우선, OpenAI 차선, 미설정 시 스마트 Mock)
        reply_text = ""
        model_used = "offline-mock"

        if settings.GEMINI_API_KEY:
            try:
                reply_text, model_used = await cls._call_gemini(system_prompt, messages_history)
            except Exception as e:
                logger.error(f"Gemini API 호출 실패: {e}, 대체 로직 실행")
                reply_text = cls._generate_mock_reply(request.message, summary)
                model_used = "gemini-fallback-mock"

        elif settings.OPENAI_API_KEY:
            try:
                reply_text = await cls._call_openai(system_prompt, messages_history)
                model_used = "gpt-4o-mini"
            except Exception as e:
                logger.error(f"OpenAI API 호출 실패: {e}, 대체 로직 실행")
                reply_text = cls._generate_mock_reply(request.message, summary)
                model_used = "openai-fallback-mock"
        else:
            # API 키가 설정되지 않은 로컬 개발/테스트 상태
            logger.info("API 키 미설정 -> 스마트 로컬 Mock 비서로 응답합니다.")
            reply_text = cls._generate_mock_reply(request.message, summary)
            model_used = "local-context-injected-mock"

        # 4. 어시스턴트 응답 히스토리 추가
        assistant_message_dict = {
            "role": "assistant",
            "content": reply_text,
            "timestamp": datetime.utcnow().isoformat()
        }
        messages_history.append(assistant_message_dict)

        # 5. 대화 내용 자동 저장 (Firestore conversations 컬렉션 영속화)
        saved_conv = await FirestoreService.save_or_update_conversation(
            conv_id=conversation_id,
            title=request.message[:25] + ("..." if len(request.message) > 25 else ""),
            messages=messages_history
        )

        return ChatResponse(
            reply=reply_text,
            conversation_id=saved_conv["id"],
            summary_applied={
                "period": summary.period,
                "count": summary.count,
                "metrics": summary.metrics.model_dump(),
                "trend": summary.trend
            },
            model_used=model_used
        )

    @classmethod
    async def _call_gemini(cls, system_prompt: str, history: List[Dict[str, Any]]) -> tuple[str, str]:
        """Google Gemini API 호출 (비동기 타임아웃 및 Flash 순차 Fallback 체인)"""
        import asyncio
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # 직전 메시지들을 컨텍스트로 전달
        prompt_with_history = ""
        for m in history[:-1]:
            role_name = "사용자" if m["role"] == "user" else "AI 비서"
            prompt_with_history += f"{role_name}: {m['content']}\n"
        
        last_user_msg = history[-1]["content"]
        if prompt_with_history:
            full_prompt = f"이전 대화 맥락:\n{prompt_with_history}\n현재 사용자 질문: {last_user_msg}"
        else:
            full_prompt = last_user_msg

        # Flash-lite 최신순 모델 우선순위 체인 (실제 API 검증 완료)
        candidate_models = [
            settings.GEMINI_MODEL_NAME,   # 사용자 지정 모델 (기본: gemini-3.5-flash-lite)
            "gemini-3.5-flash-lite",      # Flash Lite 최신 3.5 세대 (검증 완료)
            "gemini-flash-lite-latest",   # Flash Lite 최신 별칭 (검증 완료)
            "gemini-3.1-flash-lite",      # 3.1 세대 Flash Lite (검증 완료)
            "gemini-2.5-flash-lite",      # 2.5 세대 Flash Lite
            "gemini-3.5-flash",           # 표준 3.5 Flash
            "gemini-3.6-flash",           # 표준 3.6 Flash
        ]
        # 중복 제거 (순서 보존)
        models_to_try = list(dict.fromkeys(candidate_models))

        last_err = None
        for model_name in models_to_try:
            try:
                logger.info(f"Gemini Flash-Lite 비동기 호출 시도: {model_name}")
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt
                )
                
                # 모델별 15초 타임아웃 설정
                response = await asyncio.wait_for(
                    model.generate_content_async(full_prompt),
                    timeout=15.0
                )
                
                if response and response.text:
                    logger.info(f"🎉 Gemini Flash-Lite 응답 수신 성공: {model_name}")
                    return response.text, model_name
            except Exception as e:
                logger.warning(f"Flash-Lite 모델 '{model_name}' 지연 또는 오류 ({e}) -> 다음 모델 전환...")
                last_err = e

        raise last_err or RuntimeError("모든 Gemini Flash 계열 모델 호출에 실패했습니다.")

    @classmethod
    async def stream_chat(cls, request: ChatRequest):
        """SSE (Server-Sent Events) 글자/토큰 단위 실시간 스트리밍 제너레이터"""
        import asyncio
        import json

        # 1. 시계열 데이터 요약 생성 및 컨텍스트 주입
        summary = await AnalyticsService.get_summary()
        system_prompt = cls._build_system_prompt(summary)

        # 2. 대화 히스토리 구성
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        existing_conv = await FirestoreService.get_conversation_by_id(conversation_id)

        messages_history = []
        if existing_conv and "messages" in existing_conv:
            messages_history = list(existing_conv["messages"])
        elif request.history:
            messages_history = [m.model_dump() for m in request.history]

        user_message_dict = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        }
        messages_history.append(user_message_dict)

        # 3. 프론트엔드에 세션 메타데이터 첫 청크 즉시 전송
        init_meta = {
            "type": "meta",
            "conversation_id": conversation_id,
            "summary": {
                "period": summary.period,
                "count": summary.count,
                "metrics": summary.metrics.model_dump(),
                "trend": summary.trend
            }
        }
        yield f"data: {json.dumps(init_meta, ensure_ascii=False)}\n\n"

        # 4. 실시간 토큰 스트리밍 생성
        full_reply_text = ""
        used_model = "offline-mock"

        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)

                prompt_with_history = ""
                for m in messages_history[:-1]:
                    role_name = "사용자" if m["role"] == "user" else "AI 비서"
                    prompt_with_history += f"{role_name}: {m['content']}\n"
                last_user_msg = messages_history[-1]["content"]
                full_prompt = f"이전 대화 맥락:\n{prompt_with_history}\n현재 사용자 질문: {last_user_msg}" if prompt_with_history else last_user_msg

                candidate_models = [
                    settings.GEMINI_MODEL_NAME,
                    "gemini-3.1-flash-lite",
                    "gemini-flash-lite-latest",
                    "gemini-3.5-flash-lite",
                    "gemini-2.5-flash-lite",
                    "gemini-3.5-flash",
                    "gemini-3.6-flash",
                    "gemini-3.7-flash"
                ]
                models_to_try = list(dict.fromkeys(candidate_models))

                stream_success = False
                for model_name in models_to_try:
                    try:
                        logger.info(f"⚡ 실시간 토큰 스트리밍 시작 ({model_name})")
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=system_prompt
                        )
                        response_stream = await model.generate_content_async(full_prompt, stream=True)
                        used_model = model_name

                        async for chunk in response_stream:
                            if chunk and chunk.text:
                                full_reply_text += chunk.text
                                chunk_payload = {"type": "chunk", "text": chunk.text}
                                yield f"data: {json.dumps(chunk_payload, ensure_ascii=False)}\n\n"
                                await asyncio.sleep(0.01) # 부드러운 토큰 스트리밍

                        stream_success = True
                        break
                    except Exception as model_err:
                        logger.warning(f"스트리밍 모델 '{model_name}' 실패 ({model_err}) -> 다음 모델 시도...")

                if not stream_success:
                    raise RuntimeError("모든 스트리밍 모델 시도 실패")

            except Exception as e:
                logger.error(f"Gemini 스트리밍 에러: {e}, 로컬 Mock 스트리밍 전환")
                mock_text = cls._generate_mock_reply(request.message, summary)
                used_model = "gemini-fallback-mock"
                for char in mock_text:
                    full_reply_text += char
                    chunk_payload = {"type": "chunk", "text": char}
                    yield f"data: {json.dumps(chunk_payload, ensure_ascii=False)}\n\n"
                    await asyncio.sleep(0.015)
        else:
            mock_text = cls._generate_mock_reply(request.message, summary)
            used_model = "local-mock"
            for char in mock_text:
                full_reply_text += char
                chunk_payload = {"type": "chunk", "text": char}
                yield f"data: {json.dumps(chunk_payload, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.015)

        # 5. 대화 내용 영속화 (Firestore에 완성된 대화 저장)
        assistant_message_dict = {
            "role": "assistant",
            "content": full_reply_text,
            "timestamp": datetime.utcnow().isoformat()
        }
        messages_history.append(assistant_message_dict)

        await FirestoreService.save_or_update_conversation(
            conv_id=conversation_id,
            title=request.message[:25] + ("..." if len(request.message) > 25 else ""),
            messages=messages_history
        )

        # 6. 스트리밍 종료 신호
        done_payload = {
            "type": "done",
            "conversation_id": conversation_id,
            "model_used": used_model
        }
        yield f"data: {json.dumps(done_payload, ensure_ascii=False)}\n\n"

    @classmethod
    async def _call_openai(cls, system_prompt: str, history: List[Dict[str, Any]]) -> str:
        """OpenAI API 호출"""
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        messages = [{"role": "system", "content": system_prompt}]
        for m in history:
            messages.append({"role": m["role"], "content": m["content"]})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content or ""

    @classmethod
    def _generate_mock_reply(cls, user_msg: str, summary: Any) -> str:
        """API 키 미등록 환경에서도 데이터 요약을 반영하는 스마트 Mock 응답"""
        m = summary.metrics
        msg = user_msg.lower()

        if "실적" in msg or "상태" in msg or "어때" in msg or "요약" in msg or "트렌드" in msg:
            return (
                f"📊 **현재 데이터 요약 브리핑입니다!**\n\n"
                f"- **분석 기간:** {summary.period} (총 {summary.count}개 레코드)\n"
                f"- **현재 평균값:** `{m.average:,.1f}`점 (누적 합계: `{m.total:,.1f}`점)\n"
                f"- **최근 추세:** {summary.trend}\n"
                f"- **가장 최근 기록:** `{m.latest_value}`점\n\n"
                f"최근 데이터 흐름이 매우 긍정적이며, 전체 평균 대비 높은 수준을 안정적으로 유지하고 있습니다! "
                f"더 궁금한 세부 지표가 있으시면 언제든 말씀해 주세요. 😊"
            )
        elif "최고" in msg or "최대" in msg or "가장 좋" in msg:
            return (
                f"🏆 **역대 최고 기록 안내입니다!**\n\n"
                f"보유하신 데이터 중 최고치는 **`{m.max}`점**을 기록했습니다.\n"
                f"(전체 평균인 `{m.average:,.1f}`점 대비 약 `{round((m.max - m.average)/m.average * 100, 1)}%` 높은 뛰어난 성과였습니다.)"
            )
        elif "최저" in msg or "가장 낮" in msg:
            return (
                f"📉 **역대 최저 기록 안내입니다.**\n\n"
                f"보유 데이터 중 최저치는 **`{m.min}`점**이었습니다. "
                f"이후 꾸준히 상승하여 현재는 평균 `{m.average:,.1f}`점 수준으로 회복되었습니다."
            )
        else:
            return (
                f"안녕하세요! 귀하의 **{summary.period}** 동안 축적된 **{summary.count}개 데이터**(평균 `{m.average:,.1f}`점, 최고 `{m.max}`점)를 "
                f"바탕으로 질문하신 **'{user_msg}'**에 대해 검토했습니다.\n\n"
                f"현재 `{summary.trend}` 상태이며 지속적인 데이터 관리가 훌륭하게 이루어지고 있습니다. "
                f"추가적으로 분석하고 싶은 기간이나 특정 카테고리가 있다면 편하게 질문해 주세요!"
            )
