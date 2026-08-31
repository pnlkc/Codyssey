# ⚙️ Time-Series AI Assistant - Backend

Render 배포를 위한 FastAPI 백엔드 API 서비스 디렉토리입니다.

## 📁 디렉토리 구조

`	ext
backend/
├── main.py               # FastAPI 메인 엔트리포인트 및 CORS, 라우터 등록
├── config.py             # 환경변수 로드 (.env), 로거 및 Firestore 초기화
├── seed_data.py          # Firestore에 120개 초기 샘플 데이터 시딩 스크립트
├── test_backend.py       # 엔드포인트 통합 테스트 스위트
├── requirements.txt      # Python 의존성 패키지 목록
├── .python-version       # Python 버전 명시 (3.11.9)
├── .env                  # 로컬 환경변수 파일
├── .env.example          # 환경변수 템플릿
├── .gitignore            # Git 제외 설정 (보안 키 및 캐시 파일)
├── service_account.json  # Firebase 서비스 계정 키 파일 (로컬용)
├── data/
│   └── sample_timeseries.json # 120개 시계열 샘플 데이터 (초기화 및 Fallback용)
├── models/               # Pydantic 데이터 모델 (Data, Conversation, Chat)
├── routers/              # API 엔드포인트 라우터 (Data, Conversation, Chat)
├── services/             # 비즈니스 로직 계층 (Analytics, AI, Firestore)
└── README.md             # 본 가이드 문서
`

---

## 🚀 로컬 실행 방법

### 1. 가상환경 생성 및 의존성 설치
`ash
# backend 디렉토리로 이동
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 의존성 패키지 설치
pip install -r requirements.txt
`

### 2. 환경변수 설정
.env.example 파일을 복사하여 .env 파일을 구성합니다.
`ash
cp .env.example .env
`
- GEMINI_API_KEY: Google AI Studio 무료 API Key
- FIREBASE_SERVICE_ACCOUNT_PATH: service_account.json

### 3. 백엔드 서버 실행
`ash
python main.py
# 또는
uvicorn main:app --reload --port 8000
`
- 📑 **Swagger API 문서:** [http://localhost:8000/docs](http://localhost:8000/docs)
- 🩺 **Health Check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

### 4. 통합 테스트 실행
`ash
python test_backend.py
`

---

## ☁️ Render 배포 방법

1. [Render 대시보드](https://dashboard.render.com/) 접속 -> **New +** -> **Web Service** 클릭
2. GitHub 레포지토리 (`Codyssey`) 연결
3. **Web Service 설정 (중요)**:
   - **Name**: `codyssey-m1-2` (또는 원하는 이름)
   - **Language / Runtime**: `Python 3`
   - **Root Directory**: **빈칸 (공백으로 둠)** 👈 *(주의: Render는 한글 경로 입력을 거부하므로 반드시 빈칸 유지)*
   - **Build Command**: `pip install -r "M1-2/과제산출물/backend/requirements.txt"`
   - **Start Command**: `uvicorn main:app --app-dir "M1-2/과제산출물/backend" --host 0.0.0.0 --port $PORT`
4. **Environment Variables (환경 변수)** 설정:
   - `PYTHON_VERSION` = `3.11.9`
   - `GEMINI_API_KEY` = `(사용자의 Google AI Studio 키)`
   - `GEMINI_MODEL_NAME` = `gemini-3.5-flash-lite`
   - `FIREBASE_SERVICE_ACCOUNT_JSON` = `(service_account.json 내용 전체를 한 줄 JSON 문자열로 입력)`
   - `ALLOWED_ORIGINS` = `https://codyssey-m1-2.vercel.app,http://localhost:8000,http://localhost:3000,http://127.0.0.1:5500,*`
5. **Create Web Service** 클릭하여 배포 진행!
