import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from config import settings, firebase_initialized
from routers.data_router import router as data_router
from routers.conversation_router import router as conversation_router
from routers.chat_router import router as chat_router

# FastAPI 앱 생성
app = FastAPI(
    title="AI Agent: Time-Series Assistant API",
    description="시계열 데이터를 분석하고 컨텍스트를 주입하여 맞춤형 인사이트를 제공하는 나만의 AI 비서 백엔드",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 등록 (보안 화이트리스트 적용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS, # Vercel 배포 도메인 및 로컬 개발 도메인 명시적 화이트리스트
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], # 필요한 HTTP 메서드만 명시적 허용
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
)

# 라우터 등록
app.include_router(data_router)
app.include_router(conversation_router)
app.include_router(chat_router)

# 헬스체크 엔드포인트 (Render 콜드스타트 완화 및 가동 상태 확인용)
@app.api_route("/api/health", methods=["GET", "HEAD"], tags=["System"])
async def health_check():
    return {
        "status": "online",
        "firebase_connected": firebase_initialized,
        "ai_engine": f"Gemini ({settings.GEMINI_MODEL_NAME})" if settings.GEMINI_API_KEY else ("OpenAI GPT-4o-mini" if settings.OPENAI_API_KEY else "Local Mock Engine"),
        "version": "1.0.0"
    }

# 정적 파일 서빙 디렉토리 설정
current_dir = os.path.dirname(os.path.abspath(__file__))

# css, js, data 폴더 마운트
if os.path.exists(os.path.join(current_dir, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(current_dir, "css")), name="css")
if os.path.exists(os.path.join(current_dir, "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(current_dir, "js")), name="js")
if os.path.exists(os.path.join(current_dir, "data")):
    app.mount("/data", StaticFiles(directory=os.path.join(current_dir, "data")), name="data")

# 프론트엔드 메인 index.html 서빙 (GET 및 Render 헬스체크용 HEAD 지원)
@app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
async def serve_index():
    index_path = os.path.join(current_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AI Assistant Backend is Running. Visit /docs for Swagger API Documentation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
