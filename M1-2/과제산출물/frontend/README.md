# 🎨 Time-Series AI Assistant - Frontend

Vercel 배포를 위한 프론트엔드 정적 웹 애플리케이션 디렉토리입니다.

## 📁 디렉토리 구조

`	ext
frontend/
├── index.html        # 대시보드 메인 HTML UI
├── css/
│   └── style.css     # 모던 UI 테마 & 디자인 토큰 CSS
├── js/
│   ├── api.js        # FastAPI 백엔드 통신 및 SSE 스트리밍 클라이언트
│   ├── app.js        # 대시보드 인터랙션, CRUD 모달, 상태 관리
│   └── chart.js      # Canvas 기반 반응형 시계열 차트 렌더러
├── vercel.json       # Vercel 정적 호스팅 라우팅 설정
├── .vercelignore     # Vercel 배포 제외 파일
└── README.md         # 본 가이드 문서
`

---

## 🚀 로컬 실행 방법

프론트엔드는 순수 HTML/CSS/JS로 구성되어 있어 별도의 빌드 도구 없이 즉시 실행 가능합니다.

### 방법 1. VS Code Live Server 확장 프로그램
- VS Code에서 index.html 우클릭 -> **Open with Live Server** (기본 포트: 5500)
- 백엔드(http://localhost:8000)와 자동으로 연동됩니다.

### 방법 2. Python 내장 웹서버
`ash
cd frontend
python -m http.server 3000
`
- 브라우저에서 [http://localhost:3000](http://localhost:3000) 접속

---

## ☁️ Vercel 배포 방법

1. [Vercel 대시보드](https://vercel.com/) 접속 -> **Add New...** -> **Project** 클릭
2. GitHub 레포지토리 (Codyssey) 선택
3. **Project Settings (중요)**:
   - **Framework Preset**: Other
   - **Root Directory**: M1-2/과제산출물/frontend (Edit 버튼 클릭하여 선택)
   - **Build & Development Settings**: 기본값 유지 (Build Command 비워둠, Output Directory 비워둠)
4. **Deploy** 버튼 클릭!
