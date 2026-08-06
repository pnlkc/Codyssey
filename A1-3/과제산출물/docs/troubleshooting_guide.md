# ConceptNote AI 트러블슈팅 및 오류 해결 보고서 (Troubleshooting Guide)

본 문서는 `A1-3` AI 웹 서비스(ConceptNote AI) 개발 및 로컬 테스트, Vercel 배포 파이프라인 구축 과정에서 직면했던 대표 기술 오류들과 그 원인 분석 및 단계별 문제 해결 조치 내역을 상세히 기록한 보고서입니다.

---

## 1. [오류 1] Vercel CLI 프로젝트 링킹 오류 (`Detected linked project does not have "id"`)

### ❌ 현상
터미널에서 `npx vercel` 또는 `npx vercel --force` 커맨드를 실행 시 정상적인 배포 대화창이 시작되지 않고 아래 예외 메시지와 함께 비정상 종료됨:
```text
Error: An unexpected error occurred in deploy: Error: Detected linked project does not have "id".
```

### 🔍 원인 분석
- Windows 개발 환경의 Vercel 로컬 글로벌 캐시 경로(`C:\Users\<user>\AppData\Local\com.vercel.cli`)에 과거 시도 시 생성되었던 프로젝트 ID 정보가 빠진 불완전한 임시 링킹 캐시 파일이 남아 있었습니다.
- Vercel CLI가 새로 링킹(Link)하는 질문 절차를 밟지 않고 불완전한 기존 캐시 ID를 우선 참조하려고 시도하면서 예외가 발생하였습니다.

### 🛠️ 단계별 해결 조치
1. **로컬 글로벌 캐시 원천 청소**: Python 스크립트를 활용해 문제가 된 로컬 캐시 경로(`AppData\Local\com.vercel.cli`)를 완전히 삭제하여 깨진 캐시 상태를 원천 초기화 조치했습니다.
2. **CLI 신규 프로젝트 생성 및 링킹**: `npx vercel project add concept-note-ai-app` 커맨드로 Vercel 클라우드 상에 신규 프로젝트 ID를 정상 발급받고 링킹(`npx vercel link`)을 재성사시켰습니다.

### ✅ 결과 및 시사점
- `npx vercel --prod` 커맨드가 에러 없이 정상 구동되었으며 전 세계 프로덕션 배포 파이프라인이 정상 복구되었습니다.

---

## 2. [오류 2] Vercel 배포 후 웹 페이지 HTTP 404 Not Found 오류

### ❌ 현상
Vercel 라이브 배포 완료 후 제공된 URL(`https://concept-note-ai-app.vercel.app`)로 접속하면 메인 웹페이지가 서빙되지 않고 `404: NOT_FOUND` 화면이 나타남.

### 🔍 원인 분석
- 배포 설정 파일인 `vercel.json`에 아래와 같은 restrictive한 `builds` 구문이 작성되어 있었습니다:
  ```json
  "builds": [
    { "src": "api/explain.py", "use": "@vercel/python" }
  ]
  ```
- 이 구문이 Vercel 빌드 엔진에게 **"오직 `api/explain.py` 파일 하나만 제한 빌드하라"**는 명령으로 인식되어, 프로젝트 루트에 존재하는 정적 프론트엔드 파일들(`index.html`, `css/style.css`, `js/app.js` 등)이 배포 결과물 산출물에서 제외(누락)되는 원인이 되었습니다.

### 🛠️ 단계별 해결 조치
1. **`vercel.json` 라우팅 설정 구조 리팩토링**:
   제한적인 `builds` 구문을 제거하고 정적 웹 페이지 서빙과 `api/` 파이썬 라우팅을 모두 포괄하는 표준 구조로 `vercel.json`을 수정하였습니다:
   ```json
   {
     "version": 2,
     "routes": [
       { "src": "/api/(.*)", "dest": "api/$1" },
       { "src": "/(.*)", "dest": "/$1" }
     ]
   }
   ```
2. **프로덕션 재배포 구동**: `npx vercel --prod --yes` 명령으로 정적 HTML과 파이썬 서버리스 함수가 100% 모두 서빙 대상에 포함된 최신 프로덕션 빌드를 재배포하였습니다.

### ✅ 결과 및 시사점
- 배포 라이브 주소 접속 시 404가 완벽 해소되고 ConceptNote AI 메인 서비스 화면이 즉시 정상 렌더링되었습니다.

---

## 3. [오류 3] 로컬 테스트 서버 (`server.py`) 비동기 POST 핸들러 블로킹 오류

### ❌ 현상
로컬 테스트 서버(`py -3 server.py`) 구동 상태에서 화면의 [✨ AI 개념 노트 생성하기] 버튼을 눌렀을 때, 로딩 스피너만 계속해서 돌고 응답 카드 출력이 진행되지 않는 현상.

### 🔍 원인 분석
- `server.py` 내부의 `LocalDevHandler`에서 `POST /api/explain` 요청을 수신했을 때, 백엔드 핸들러 클래스(`ExplainHandler`)를 재인스턴스화하는 방식으로 위임하려 했습니다.
- 이 과정에서 `BaseHTTPRequestHandler.__init__`이 소켓 I/O 헤더 파싱을 중복 수행하려 시도하면서 메인 스레드가 블로킹(무한 대기) 상태에 빠졌습니다.

### 🛠️ 단계별 해결 조치
- `server.py` 내부에서 중복 핸들러 인스턴스화 대신 `api/explain.py`의 비즈니스 로직 함수(`load_env`, `call_gemini_api`, `parse_json_from_llm`)를 직접 호출하여 파싱 및 HTTP 200 JSON 응답을 즉시 반환하도록 로컬 서버 핸들러를 리팩토링하였습니다.

### ✅ 결과 및 시사점
- 폼 제출 후 2~3초 내에 Gemini AI가 분석한 개념 카드가 멈춤 없이 즉시 화면에 출력되었습니다.

---

## 4. [오류 4] 브라우저 `favicon.ico` 404 경고 수신

### ❌ 현상
로컬 서버 콘솔에 `GET /favicon.ico 404` 로그 메세지가 정기적으로 출력됨.

### 🔍 원인 분석
- 웹 브라우저가 사이트 탭 상단에 표기할 파비콘 아이콘을 자동으로 요청했으나 관련 파일이 존재하지 않아 나타난 무해한 404 메세지였습니다.

### 🛠️ 단계별 해결 조치
- `index.html` 헤더 영역에 inline SVG 파비콘 태그를 주입해 브라우저가 별도의 파일 요청 없이 파비콘을 즉시 로드하도록 조치했습니다:
  ```html
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💡</text></svg>">
  ```

---

## 5. 종합 평가 및 결론

본 프로젝트는 AI 코딩 도구를 활용함과 동시에 직면했던 **CLI 로컬 캐시 링킹 버그, Vercel 빌더의 정적 파일 누락 404, 파이썬 서버 소켓 블로킹 현상**을 원인 분석 기반으로 체계적으로 해결하였습니다. 이러한 트러블슈팅 경험은 서비스의 로컬 테스트 무결성과 클라우드 자동 배포 안정성을 동시에 확보하는 기회가 되었습니다.
