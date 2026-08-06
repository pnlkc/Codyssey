# A1-2 CLI 국내 여행지 추천 및 리포트 생성 프로그램

Google Gemini LLM API와 Kakao Local 장소 검색 API를 연동하여 사용자가 입력한 여행 날짜에 맞춰 국내 여행지를 추천하고 맛집 정보를 검색하여 풍부한 여행 리포트를 자동 생성하는 CLI 기반 Python 프로그램입니다.

---

## 1. 프로그램 개요

- **CLI 인터페이스**: `argparse` 기반으로 `-date "YYYY-MM-DD"` 필수 옵션을 수신하며 날짜 형식을 자동 검증합니다.
- **1차 추천 (LLM API)**: 여행 날짜 시기에 적합한 국내 추천 도시(`recommended_city`), 날씨 요약(`weather`), 주요 행사/축제(`events`), 추천 이유(`reason`)를 파싱합니다. 파싱 실패 시 프롬프트를 보정하여 **1회 자동 재시도**합니다.
- **맛집 검색 (지도 API)**: 추천 도시 기반으로 Kakao Local REST API를 호출하여 맛집 5곳의 정보(상호명, 주소, 카테고리, 장소 URL, 좌표)를 검색합니다. (검색 실패/인증 오류/0건 발생 시 예외 처리하여 프로그램이 중단되지 않고 `errors` 목록에 기록 후 다음 단계 진행)
- **최종 여행 리포트 생성 (LLM API)**: 추천 정보와 맛집 검색 결과(0건 포함) 및 오류 요약을 종합하여 Markdown 규격 여행 리포트를 생성합니다.
- **결과 저장**: `results/` 폴더 하위에 원본 JSON 데이터(`{date}_travel_plan_raw.json`)와 최종 Markdown 리포트(`{date}_travel_plan.md`)를 자동 저장합니다.

---

## 2. 개발 환경 및 요구 사항

- **Python 버전**: Python 3.10 이상
- **외부 패키지**: 기본 내장 라이브러리(`urllib`, `json`, `argparse`, `re` 등)로 동작 가능하도록 작성되어 있습니다. `.env` 파일 관리를 위해 `python-dotenv` 사용을 권장합니다.

---

## 3. API 키 발급 및 설정 방법 (보안 주의사항)

> [!CAUTION]
> **API 키 보안 주의사항**
> - API 키는 절대 코드나 제출물(Git 커밋, README 등)에 직접 노출해서는 안 됩니다.
> - 프로젝트 루트 하위의 `.env` 파일 또는 시스템 환경 변수로 관리해야 합니다.

### (1) API 키 발급
1. **Google Gemini API**: [Google AI Studio](https://aistudio.google.com/)에서 Gemini API Key 발급
2. **Kakao Local API**: [Kakao Developers](https://developers.kakao.com/)에서 내 애플리케이션 등록 후 **REST API 키** 확인

### (2) `.env` 파일 설정 방법
프로젝트 디렉토리(`A1-2/과제산출물/`) 내에 `.env` 파일을 생성하고 아래와 같이 키를 설정합니다. (`.env.example` 참조)

```env
GEMINI_API_KEY=your_actual_gemini_api_key
KAKAO_REST_API_KEY=your_actual_kakao_rest_api_key
```

### (3) 환경 변수 직접 설정 방법 (선택)
- **Windows PowerShell**:
  ```powershell
  $env:GEMINI_API_KEY="your_actual_gemini_api_key"
  $env:KAKAO_REST_API_KEY="your_actual_kakao_rest_api_key"
  ```
- **macOS / Linux**:
  ```bash
  export GEMINI_API_KEY="your_actual_gemini_api_key"
  export KAKAO_REST_API_KEY="your_actual_kakao_rest_api_key"
  ```

---

## 4. 실행 방법

```bash
# Windows 환경 실행 (권장)
py -3 main.py -date "2026-03-15"

# 일반 python 명령어 실행
python main.py -date "2026-03-15"

# 호환 진입점 실행 (travel_planner.py)
py -3 travel_planner.py -date "2026-03-15"
```

### 날짜 입력 예외 처리 테스트
```bash
python main.py -date "invalid-date"
# 출력: 오류: 'invalid-date'는 올바른 날짜 형식이 아닙니다. (YYYY-MM-DD 형식 필요)
```

---

## 5. 결과물 확인 방법

프로그램 실행이 완료되면 `results/` 폴더에 다음과 같은 결과물이 생성됩니다.

1. **원본 데이터 JSON**: `results/2026-03-15_travel_plan_raw.json`
   - 1차 추천 파싱 결과, 맛집 검색 결과 목록, `errors` 배열 포함
2. **최종 여행 리포트 Markdown**: `results/2026-03-15_travel_plan.md`
   - 추천 지역, 추천 이유, 날씨 요약, 행사/축제, 맛집 추천 목록(0건 시 "데이터 없음"), 1일 일정 제안 포함

---

## 6. 아키텍처 및 핵심 설계 설명 (평가 질문 참조)

1. **모듈/함수 분리 구조**:
   - `generate_first_recommendation()`: LLM 1차 추천 및 JSON 파싱/재시도
   - `search_places_kakao()`: Kakao Local API 장소 검색 및 예외 처리
   - `generate_final_markdown_report()`: 최종 마크다운 리포트 생성
   - `save_results()`: 결과 파일 일괄 저장
2. **장소 API 제공자 변경 가용성**:
   - `search_places_kakao()`와 같은 독립 장소 검색 함수로 캡슐화하여 Naver Local 등 타 지도 API로 교체 시에도 메인 제어 흐름 수정 없이 검색 함수 내부만 교체할 수 있습니다.
3. **에러 누적 및 데이터 없음 처리**:
   - 지도 API 호출 중 401/403 인증 실패나 검색 결과 0건 등 모든 예외 상황을 `errors` 리스트에 표준화된 객체(`{"step": ..., "type": ..., "message": ...}`)로 누적 기록하며, 맛집 항목을 "데이터 없음"으로 안전하게 Fallback 처리합니다.
4. **JSON 강제 출력 및 재시도 프롬프트 전략**:
   - LLM에 JSON 스키마를 프롬프트로 명시하고 `parse_json_response()`에서 필수 키 존재 여부를 검증합니다. 실패 시 1회에 한해 "순수 JSON 형식 강제" 프롬프트를 재전송하여 파싱 성공률을 확보합니다.
