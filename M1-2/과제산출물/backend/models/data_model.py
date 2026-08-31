from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class DataCreate(BaseModel):
    date: str = Field(..., description="날짜 (YYYY-MM-DD)", examples=["2026-02-25"])
    value: float = Field(..., description="수치 데이터 (실적/학습시간/매출 등)", examples=[850.0])
    memo: str = Field(..., description="메모 또는 설명", examples=["최종 배포 테스트 완료"])
    category: Optional[str] = Field("일반", description="카테고리 분류", examples=["개발"])

class DataUpdate(BaseModel):
    date: Optional[str] = Field(None, description="수정할 날짜 (YYYY-MM-DD)", examples=["2026-02-25"])
    value: Optional[float] = Field(None, description="수정할 수치", examples=[900.0])
    memo: Optional[str] = Field(None, description="수정할 메모", examples=["일정 갱신"])
    category: Optional[str] = Field(None, description="수정할 카테고리", examples=["개발"])

class DataResponse(BaseModel):
    id: str = Field(..., description="고유 ID")
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")
    value: float = Field(..., description="수치 데이터")
    memo: str = Field(..., description="메모")
    category: Optional[str] = Field("일반", description="카테고리")
    created_at: Optional[str] = Field(None, description="생성 시각 (ISO format)")

class DataSummaryMetrics(BaseModel):
    total: float = Field(..., description="총합계")
    average: float = Field(..., description="평균값")
    max: float = Field(..., description="최댓값")
    min: float = Field(..., description="최솟값")
    latest_value: Optional[float] = Field(None, description="최근 데이터값")

class DataSummaryResponse(BaseModel):
    period: str = Field(..., description="데이터 기간", examples=["2025-11 ~ 2026-02"])
    count: int = Field(..., description="총 데이터 개수", examples=[120])
    metrics: DataSummaryMetrics = Field(..., description="통계 지표 객체")
    trend: str = Field(..., description="최근 추세 요약", examples=["상승 (최근 7일 평균 대비 +15%)"])
    raw_summary_text: Optional[str] = Field(None, description="시스템 프롬프트 주입용 서식화 텍스트")
