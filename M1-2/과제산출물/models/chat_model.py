from pydantic import BaseModel, Field
from typing import Optional, List
from .conversation_model import Message

class ChatRequest(BaseModel):
    message: str = Field(..., description="사용자 질문/입력", examples=["최근 실적 추세와 최고 실적 날짜를 알려줘"])
    conversation_id: Optional[str] = Field(None, description="기존 대화 세션 ID (없으면 신규 대화 생성)")
    history: Optional[List[Message]] = Field(default_factory=list, description="이전 대화 맥락")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI 비서 맞춤 답변")
    conversation_id: str = Field(..., description="대화 세션 ID")
    summary_applied: Optional[dict] = Field(None, description="프롬프트에 주입된 데이터 요약 정보")
    model_used: Optional[str] = Field(None, description="사용된 AI 모델 이름")
