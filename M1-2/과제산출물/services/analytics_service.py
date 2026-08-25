import logging
from typing import List, Dict, Any
from models.data_model import DataSummaryResponse, DataSummaryMetrics
from services.firestore_service import FirestoreService

logger = logging.getLogger("analytics_service")

class AnalyticsService:
    """시계열 데이터 분석 및 프롬프트 주입용 요약 생성 서비스"""

    @staticmethod
    async def get_summary() -> DataSummaryResponse:
        """저장된 전체 시계열 데이터를 분석하여 요약 정보 반환"""
        data_list = await FirestoreService.get_all_data()

        if not data_list:
            # 데이터가 비어있을 때의 기본 안전 응답
            metrics = DataSummaryMetrics(total=0.0, average=0.0, max=0.0, min=0.0, latest_value=0.0)
            return DataSummaryResponse(
                period="데이터 없음",
                count=0,
                metrics=metrics,
                trend="데이터 없음 (신규 등록 필요)",
                raw_summary_text="현재 등록된 데이터가 없습니다."
            )

        # 날짜순 정렬
        sorted_data = sorted(data_list, key=lambda x: x.get("date", ""))
        values = [float(item.get("value", 0)) for item in sorted_data]
        dates = [item.get("date", "") for item in sorted_data]

        count = len(values)
        start_date = dates[0] if dates else "알 수 없음"
        end_date = dates[-1] if dates else "알 수 없음"
        period = f"{start_date} ~ {end_date}"

        total = round(sum(values), 2)
        average = round(total / count, 2) if count > 0 else 0.0
        max_val = round(max(values), 2) if count > 0 else 0.0
        min_val = round(min(values), 2) if count > 0 else 0.0
        latest_val = values[-1] if count > 0 else 0.0

        # 트렌드(추세) 분석 알고리즘
        # 최근 7개(또는 최근 10%) 데이터의 평균과 전체 평균 비교
        recent_window = min(7, count)
        recent_values = values[-recent_window:]
        recent_avg = sum(recent_values) / recent_window if recent_window > 0 else average

        diff_ratio = ((recent_avg - average) / average * 100) if average > 0 else 0.0

        if diff_ratio > 5:
            trend = f"상승 추세 (최근 {recent_window}일 평균 {round(recent_avg, 1)} / 전체 평균 대비 +{round(diff_ratio, 1)}%)"
        elif diff_ratio < -5:
            trend = f"하강 추세 (최근 {recent_window}일 평균 {round(recent_avg, 1)} / 전체 평균 대비 {round(diff_ratio, 1)}%)"
        else:
            trend = f"안정/유지 추세 (최근 {recent_window}일 평균 {round(recent_avg, 1)} / 전체 평균과 유사)"

        # 최고치 기록 일자 및 메모 탐색
        max_item = max(sorted_data, key=lambda x: float(x.get("value", 0))) if sorted_data else {}
        max_info = f"{max_item.get('date')} ({max_item.get('value')}점 - {max_item.get('memo', '')})"

        # 시스템 프롬프트 주입용 텍스트 조립
        raw_summary_text = (
            f"=== [사용자 시계열 데이터 요약 보고서] ===\n"
            f"- 데이터 분석 기간: {period}\n"
            f"- 총 레코드 수: {count}개\n"
            f"- 누적 합계: {total:,.2f}\n"
            f"- 전체 평균값: {average:,.2f}\n"
            f"- 역대 최고치: {max_val} (일자: {max_info})\n"
            f"- 역대 최저치: {min_val}\n"
            f"- 가장 최근 데이터: {latest_val} (날짜: {end_date})\n"
            f"- 최근 트렌드: {trend}\n"
            f"====================================="
        )

        metrics = DataSummaryMetrics(
            total=total,
            average=average,
            max=max_val,
            min=min_val,
            latest_value=latest_val
        )

        return DataSummaryResponse(
            period=period,
            count=count,
            metrics=metrics,
            trend=trend,
            raw_summary_text=raw_summary_text
        )
