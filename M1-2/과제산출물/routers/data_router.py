from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from models.data_model import DataCreate, DataUpdate, DataResponse, DataSummaryResponse
from services.firestore_service import FirestoreService
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/data", tags=["Data Management"])

@router.get("/summary", response_model=DataSummaryResponse, summary="시계열 데이터 통계 요약")
async def get_data_summary():
    """저장된 시계열 데이터의 기간, 총합, 평균, 최고/최저치 및 최근 추세(Trend)를 분석하여 반환합니다."""
    return await AnalyticsService.get_summary()

@router.post("", response_model=DataResponse, status_code=status.HTTP_201_CREATED, summary="새 데이터 등록")
async def create_data(payload: DataCreate):
    """새로운 일일 시계열 데이터(date, value, memo, category)를 Firestore에 등록합니다."""
    try:
        created = await FirestoreService.create_data(payload)
        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 생성 실패: {str(e)}")

@router.get("", response_model=List[DataResponse], summary="데이터 목록 조회")
async def get_data_list(
    limit: Optional[int] = Query(None, description="가져올 최대 개수"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$", description="정렬 순서 (날짜 기준)")
):
    """전체 시계열 데이터 목록을 조회합니다."""
    data_list = await FirestoreService.get_all_data()
    if order == "desc":
        data_list = sorted(data_list, key=lambda x: x.get("date", ""), reverse=True)
    else:
        data_list = sorted(data_list, key=lambda x: x.get("date", ""))
    
    if limit:
        data_list = data_list[:limit]
    return data_list

@router.get("/{id}", response_model=DataResponse, summary="특정 데이터 상세 조회")
async def get_data_item(id: str):
    """지정된 ID의 데이터를 단건 조회합니다."""
    item = await FirestoreService.get_data_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="해당 ID의 데이터를 찾을 수 없습니다.")
    return item

@router.put("/{id}", response_model=DataResponse, summary="데이터 수정")
async def update_data(id: str, payload: DataUpdate):
    """지정된 ID의 데이터를 수정합니다."""
    updated = await FirestoreService.update_data(id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="수정할 데이터를 찾을 수 없습니다.")
    return updated

@router.delete("/{id}", summary="데이터 삭제")
async def delete_data(id: str):
    """지정된 ID의 데이터를 삭제합니다."""
    deleted = await FirestoreService.delete_data(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="삭제할 데이터를 찾을 수 없습니다.")
    return {"status": "success", "message": f"데이터({id})가 성공적으로 삭제되었습니다."}
