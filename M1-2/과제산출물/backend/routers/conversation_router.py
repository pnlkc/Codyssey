from fastapi import APIRouter, HTTPException, status
from typing import List
from models.conversation_model import ConversationCreate, ConversationResponse
from services.firestore_service import FirestoreService

router = APIRouter(prefix="/api/conversations", tags=["Conversations Management"])

@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED, summary="대화 세션 저장")
async def create_conversation(payload: ConversationCreate):
    """새로운 대화 세션과 메시지들을 저장합니다."""
    try:
        messages_dict = [m.model_dump() for m in payload.messages]
        saved = await FirestoreService.save_or_update_conversation(
            conv_id=None,
            title=payload.title,
            messages=messages_dict
        )
        return saved
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대화 저장 실패: {str(e)}")

@router.get("", response_model=List[ConversationResponse], summary="대화 목록 조회")
async def get_conversations_list():
    """저장된 전체 대화 목록을 최신순으로 조회합니다."""
    return await FirestoreService.get_all_conversations()

@router.get("/{id}", response_model=ConversationResponse, summary="특정 대화 상세 조회 (대화 불러오기)")
async def get_conversation_detail(id: str):
    """지정된 대화의 전체 메시지 히스토리를 조회하여 이전 대화를 복원합니다."""
    conv = await FirestoreService.get_conversation_by_id(id)
    if not conv:
        raise HTTPException(status_code=404, detail="해당 대화 세션을 찾을 수 없습니다.")
    return conv

@router.delete("/{id}", summary="대화 삭제")
async def delete_conversation(id: str):
    """지정된 ID의 대화 기록을 삭제합니다."""
    deleted = await FirestoreService.delete_conversation(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="삭제할 대화를 찾을 수 없습니다.")
    return {"status": "success", "message": f"대화({id})가 성공적으로 삭제되었습니다."}
