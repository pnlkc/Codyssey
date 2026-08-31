from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    role: str = Field(..., description="메시지 역할 (user / assistant / system)", examples=["user"])
    content: str = Field(..., description="메시지 내용", examples=["이번 달 실적이 어때?"])
    timestamp: Optional[str] = Field(None, description="메시지 전송 시각")

class ConversationCreate(BaseModel):
    title: Optional[str] = Field("새로운 대화", description="대화 세션 제목")
    messages: List[Message] = Field(default_factory=list, description="대화 메시지 목록")

class ConversationResponse(BaseModel):
    id: str = Field(..., description="대화 고유 ID")
    title: str = Field(..., description="대화 세션 제목")
    messages: List[Message] = Field(default_factory=list, description="대화 메시지 목록")
    message_count: Optional[int] = Field(0, description="메시지 개수")
    created_at: Optional[str] = Field(None, description="생성 시각")
    updated_at: Optional[str] = Field(None, description="최종 업데이트 시각")
