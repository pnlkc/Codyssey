# Changelog

## [v1.2] - 2026-05-28 - [수행 주체: Antigravity AI]

**작업 내용:**
- `llm_comparison_report.md` 전면 재작성
- `system_design_document.md` 전면 재작성

**사유:**
- 이전 버전의 두 문서에 `raw_execution_log.txt` 실제 Raw 데이터와 불일치하는 내용 다수 확인됨.
- 주요 오류 목록:
  - `llm_comparison_report.md`: 섹션 4.1 평가 축 정의가 플레이스홀더(`[ 예: ... ]`) 텍스트로 미작성 상태
  - `system_design_document.md`: CoT ※ 주의 문구에 "1~3단계"로 오기 (실제 Raw에는 4단계) → "1~4단계"로 정정
  - `system_design_document.md`: 환각 Q2 질문이 가명 처리된 버전으로 기재되어 있으나, Raw에서는 실명("이영희 대리") 포함 질문이었으므로 실제 Raw 기준으로 정정
  - `system_design_document.md`: 환각 Q3 PASS 판정 근거에 Turn 7 최종 결정(보안 적용 제외) 미반영
  - `system_design_document.md`: 프롬프트 개선 이력에 v1.5(Few-shot 단계) 버전 누락
  - `llm_comparison_report.md`: 섹션 5 정성 평가에서 GPT 5 표 포맷 준수 실패 근거가 Raw와 불일치
- 사용자 지시: "raw 응답 기반으로 md 파일 두 개 다시 작성해줘"

**검증 결과:**
- 두 파일 모두 `raw_execution_log.txt` (PART 1~5 전문) 기준으로 내용 교차 검증 후 재작성 완료.
- 환각 없이 Raw 데이터에 기재된 실제 응답·수치·판정 결과만 반영.

---

## [v1.1] - 2026-05-28 - [수행 주체: Antigravity AI]

**작업 내용:**
- `raw_execution_log.txt` 정리 및 전체 10턴 멀티턴 대화 + 환각 검증 5개 원본 응답 누적 기록 완료
- `llm_comparison_report.md` 섹션 5 정성 평가 부분 초안 작성
- `system_design_document.md` 섹션 4.3 v1 vs v2 CoT 비교 표 초안 작성

**사유:**
- Zero-shot(PART 1), Few-shot(PART 2), CoT(PART 3), 10턴 멀티턴(PART 4), 환각 검증(PART 5) 순서로 실험 전 단계 완료 후 Raw 로그 통합 기록 필요

**검증 결과:**
- Raw 로그 작성 완료 (652라인). 일부 섹션은 Raw 데이터와 미세 불일치로 v1.2에서 재정정 처리됨.

---

## [v1.0] - 2026-05-28 - [수행 주체: Antigravity AI]

**작업 내용:**
- 프로젝트 초기 파일 구조 생성
- `llm_comparison_report.md` 초안 생성 (템플릿 기반)
- `system_design_document.md` 초안 생성 (템플릿 기반)
- `raw_execution_log.txt` 파일 생성 및 실험 데이터 누적 시작

**사유:**
- 스마트 스토어 고도화 프로젝트 회의록 자동 요약 시스템 구축을 위한 LLM 비교·선정 실험 착수

**검증 결과:**
- 초안 단계로 플레이스홀더 포함. 실험 진행 후 순차 업데이트 예정.
