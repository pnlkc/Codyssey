# ConceptNote AI 개발 증빙 및 검증 자료 (Screenshots & AI Logs)

본 문서는 A1-3 과제 제출 요구사항 중 **증빙 자료(서비스 스크린샷 세트 및 AI 코딩 도구 활용 대화 로그)**를 정리한 설명서입니다.

---

## 1. 서비스 스크린샷 증빙 세트

실제 배포 URL 또는 로컬 구동 화면에서 아래 3가지 장면의 스크린샷을 첨부하여 제출합니다.

### 📸 (1) 데스크톱 웹 메인 화면 (Desktop View)
- **설명**: Hero 섹션, GNB 네비게이션 메뉴 및 4개 메인 섹션이 깔끔하게 표시되는 데스크톱 해상도 화면
- **확인 항목**: 메인 타이틀, AI 개념 생성 폼, 통계 수치 및 레이아웃 정렬 상태

### 📱 (2) 모바일 반응형 레이아웃 화면 (Mobile View)
- **설명**: 모바일 뷰포트(너비 375px~430px) 환경에서 레이아웃 깨짐 없이 렌더링된 화면
- **확인 항목**: 1열 반응형 그리드 전환, 폼 요소 자동 맞춤, 가로 스크롤 생성 여부

### 🤖 (3) AI 개념 노트 생성 및 저장 동작 화면 (AI Action View)
- **설명**: 키워드 입력 후 AI가 '핵심 정의, 주요 특징, 쉬운 비유, 예시 코드'를 카드 형태로 정상 출력하고 내 메모장에 저장된 화면
- **확인 항목**: 결과 카드의 4개 구조화 블록 렌더링 및 내 저장 메모장 카드 추가 상태

---

## 2. AI 코딩 도구 활용 프롬프트 및 대화 로그 증빙

### 💬 대화 로그 예시 1: 프론트엔드 및 AI 개념 메모장 UI 구축
> **사용자 프롬프트**:
> "특정 키워드를 입력하면 해당 키워드에 대한 개념적 설명을 자동으로 작성해서 학습 가능한 AI 학습 메모장 웹 서비스를 바닐라 HTML/CSS/JS로 만들어줘. 3개 이상의 섹션을 포함하고 반응형이어야 해."
>
> **AI 응답 및 적용 요약**:
> - `index.html`: Hero, AI 개념 생성, 내 저장 노트, FAQ 등 4개 섹션 구조 정의
> - `css/style.css`: 현대적인 Glassmorphism 다크 테마 및 미디어 쿼리 기반 반응형 CSS 스타일 작성
> - `js/app.js`: DOM 이벤트 핸들러, 빈 입력 파싱 검증, LocalStorage 연동 노트 저장/삭제 기능 구현

---

### 💬 대화 로그 예시 2: Vercel Serverless Function (Python) 백엔드 연동
> **사용자 프롬프트**:
> "Vercel Serverless Function (Python)을 활용해 `api/explain.py` 백엔드를 구축하고 Gemini API (`gemini-3.5-flash-lite`)를 연동하여 JSON으로 응답하게 해줘."
>
> **AI 응답 및 적용 요약**:
> - `api/explain.py`: WSGI BaseHTTPRequestHandler 기반 `do_POST` 파라미터 파싱 및 Gemini REST API 호출
> - JSON 강제 지정 및 JSONDecodeError 처리, CORS 헤더 지원 및 API 키 보안 처리 완수
