from fastapi import APIRouter, HTTPException, status
from models.chat_model import ChatRequest, ChatResponse
from services.ai_service import AIService

router = APIRouter(prefix="/api/chat", tags=["AI Chatbot"])

@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK, summary="데이터 기반 AI 챗봇 대화")
async def chat_with_assistant(payload: ChatRequest):
    """
    사용자의 질문을 수신하고, Firestore에 저장된 시계열 데이터 요약(/api/data/summary)을 
    시스템 프롬프트에 실시간 주입한 뒤 Gemini/OpenAI를 호출하여 맞춤형 인사이트 답변을 제공합니다.
    (대화 내용은 Firestore 'conversations' 컬렉션에 자동 저장됩니다.)
    """
    try:
        response = await AIService.chat(payload)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 대화 처리 실패: {str(e)}")
