import os
import json
import logging
from typing import Optional, List
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("config")

# .env 파일 명시적 절대경로 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, ".env")
if os.path.exists(env_file_path):
    load_dotenv(env_file_path, override=True)
load_dotenv(override=True)

class Settings:
    # 포트 및 호스트
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # CORS 허용 목록 (기본 화이트리스트)
    ALLOWED_ORIGINS_RAW: str = os.getenv(
        "ALLOWED_ORIGINS",
        "https://codyssey-m1-2.vercel.app,http://localhost:8000,http://localhost:3000,http://127.0.0.1:5500,http://127.0.0.1:8000,*"
    )
    
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]

    # AI API Keys & Models
    GEMINI_API_KEY_RAW: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    @property
    def GEMINI_API_KEY(self) -> Optional[str]:
        if not self.GEMINI_API_KEY_RAW:
            return None
        cleaned = self.GEMINI_API_KEY_RAW.strip().strip("'\"")
        return cleaned if cleaned and cleaned != "your_gemini_api_key_here" else None

    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-3.6-flash").strip().strip("'\"")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Firebase 설정
    FIREBASE_SERVICE_ACCOUNT_PATH: Optional[str] = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH",
        os.path.join(current_dir, "service_account.json")
    )
    FIREBASE_SERVICE_ACCOUNT_JSON: Optional[str] = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

settings = Settings()

# Firebase Firestore 초기화
db = None
firebase_initialized = False

try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    cred = None
    # 1. 환경변수 JSON 문자열 우선 확인 (Render 배포용)
    if settings.FIREBASE_SERVICE_ACCOUNT_JSON:
        try:
            cert_dict = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
            cred = credentials.Certificate(cert_dict)
            logger.info("Firebase: 환경변수 JSON 문자열로부터 자격증명 로드 완료")
        except Exception as e:
            logger.warning(f"Firebase JSON 파싱 실패: {e}")

    # 2. 로컬 파일 경로 확인
    if not cred and settings.FIREBASE_SERVICE_ACCOUNT_PATH and os.path.exists(settings.FIREBASE_SERVICE_ACCOUNT_PATH):
        try:
            cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
            logger.info(f"Firebase: 파일({settings.FIREBASE_SERVICE_ACCOUNT_PATH})로부터 자격증명 로드 완료")
        except Exception as e:
            logger.warning(f"Firebase 파일 자격증명 로드 실패: {e}")

    # Firebase 앱 초기화
    if cred:
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        firebase_initialized = True
        logger.info("Firebase Firestore 초기화 성공!")
    else:
        logger.info("Firebase 서비스 계정 키 미설정 -> 로컬 In-Memory / JSON Fallback 스토리지로 자동 구동됩니다.")
except Exception as e:
    logger.warning(f"Firebase SDK 로드 중 예외 발생: {e} (로컬 Fallback 스토리지 사용)")
