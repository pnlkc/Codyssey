# ConceptNote AI - AI 스마트 개념 학습 메모장

ConceptNote AI는 사용자가 학습하고자 하는 기술 용어, 프로그래밍 개념, 일반 지식 키워드를 입력하면 Google Gemini LLM API가 핵심 정의, 주요 특징, 쉬운 비유, 예시 코드를 포함한 맞춤형 개념 학습 노트를 자동으로 생성하고 관리해주는 인터랙티브 웹 서비스입니다.

---

## 1. 프로젝트 개요

- **웹 서비스명**: ConceptNote AI (AI 스마트 개념 학습 메모장)
- **공식 Vercel 배포 URL**: [https://concept-note-ai-app.vercel.app](https://concept-note-ai-app.vercel.app)
- **주요 기능**:
  - 키워드 및 난이도 선택 입력
  - Vercel Serverless Function (`api/explain.py`)을 통한 Gemini AI 개념 분석 및 카드 생성
  - 4개 주요 섹션 (Hero 소개, 개념 노트 생성, 내 저장 메모장, FAQ) 및 반응형 UI
  - 로컬 스토리지(`localStorage`) 연동으로 나만의 개념 노트 저장/관리
  - 빈 입력, API 에러(4xx/5xx), 네트워크 지연 시 사용자 안내 메시지(Toast / Alert) 제공

---

## 2. 기술 스택

- **Front-end**: Vanilla HTML5, CSS3 (Modern Glassmorphism & Responsive Layout), JavaScript (ES6+)
- **Back-end**: Vercel Serverless Functions (Python 3.10+)
- **AI API**: Google Gemini REST API (`gemini-3.5-flash-lite`)
- **Deployment**: Vercel (GitHub 저장소 연동 자동 CI/CD 배포)

---

## 3. API 키 발급 및 `.env` 설정 (보안 가이드)

> [!CAUTION]
> API 키는 절대 소스코드나 README, 스크린샷에 노출해서는 안 됩니다.

1. [Google AI Studio](https://aistudio.google.com/)에서 Gemini API 키를 발급받습니다.
2. 프로젝트 루트(`A1-3/과제산출물/`)에 `.env` 파일을 생성합니다.
3. 아래와 같이 환경변수를 작성합니다.

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 4. 실행 및 배포 방법

### (1) 로컬 환경 실행
1. 웹 서버 또는 VS Code Live Server 등을 이용해 `index.html`을 구동합니다.
2. 백엔드 테스트를 위해 Python 3.10+ 환경에서 `api/explain.py` 서버리스 핸들러를 호스팅하거나 Vercel CLI (`vercel dev`)를 구동합니다.

```bash
# Vercel CLI 로컬 개발 구동
vercel dev
```

### (2) Vercel 배포 방법
1. 프로젝트를 GitHub 저장소에 푸시합니다.
2. Vercel 대시보드에서 해당 저장소를 임포트(Import)합니다.
3. Vercel 프로젝트 설정의 **Environment Variables** 메뉴에서 `GEMINI_API_KEY` 값을 등록합니다.
4. 배포(Deploy) 버튼을 누르면 나만의 라이브 URL이 생성됩니다.

---

## 5. 제출 패키지 5종 구성

  1. **배포 및 구동 웹 앱**: `index.html`, `css/style.css`, `js/app.js`, `api/explain.py`
  2. **GitHub 저장소 구조**: 프론트엔드와 백엔드(`api/`)가 구분된 표준 디렉토리 구조
  3. **README.md**: 본 설명 문서
  4. **서비스 기획서**: `service_plan.md` (목적, 타겟, 4개 섹션 구성, AI 기능 입출력 & 예외 처리 기준)
  5. **증빙 자료 & 트러블슈팅**: `docs/screenshots_and_logs.md` (증빙 자료) 및 [docs/troubleshooting_guide.md](docs/troubleshooting_guide.md) (오류 해결 가이드)
