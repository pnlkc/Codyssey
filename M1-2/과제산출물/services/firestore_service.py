import json
import os
import uuid
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from config import db, firebase_initialized
from models.data_model import DataCreate, DataUpdate, DataResponse
from models.conversation_model import ConversationCreate, ConversationResponse, Message

try:
    from firebase_admin import firestore
except ImportError:
    try:
        from google.cloud import firestore
    except ImportError:
        firestore = None

logger = logging.getLogger("firestore_service")

# 로컬 샘플 데이터 파일 경로
SAMPLE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_timeseries.json")

# In-Memory Fallback 스토리지 (Firebase 미연동 시 활용)
_memory_data: Dict[str, Dict[str, Any]] = {}
_memory_conversations: Dict[str, Dict[str, Any]] = {}

def _init_local_fallback():
    """로컬 데이터셋을 메모리에 로드"""
    global _memory_data
    if os.path.exists(SAMPLE_DATA_PATH):
        try:
            with open(SAMPLE_DATA_PATH, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    _memory_data[item["id"]] = item
            logger.info(f"로컬 Fallback 스토리지: {len(_memory_data)}개 샘플 데이터 로드 완료")
        except Exception as e:
            logger.error(f"샘플 데이터 로드 실패: {e}")

_init_local_fallback()

class FirestoreService:
    """Firestore 데이터베이스 연동 및 로컬 Fallback 서비스"""

    # -------------------------------------------------------------
    # 1. 시계열 데이터 (data 컬렉션) CRUD
    # -------------------------------------------------------------
    @staticmethod
    async def get_all_data() -> List[Dict[str, Any]]:
        """모든 시계열 데이터 조회 (날짜 오름차순 정렬)"""
        if firebase_initialized and db:
            try:
                docs = db.collection("data").order_by("date").stream()
                result = []
                for doc in docs:
                    d = doc.to_dict()
                    d["id"] = doc.id
                    result.append(d)
                return result
            except Exception as e:
                logger.error(f"Firestore get_all_data 에러: {e}")
        
        # Fallback
        items = list(_memory_data.values())
        items.sort(key=lambda x: x.get("date", ""))
        return items

    @staticmethod
    async def get_data_by_id(data_id: str) -> Optional[Dict[str, Any]]:
        """특정 ID의 데이터 조회"""
        if firebase_initialized and db:
            try:
                doc = db.collection("data").document(data_id).get()
                if doc.exists:
                    d = doc.to_dict()
                    d["id"] = doc.id
                    return d
                return None
            except Exception as e:
                logger.error(f"Firestore get_data_by_id 에러: {e}")

        # Fallback
        return _memory_data.get(data_id)

    @staticmethod
    async def create_data(payload: DataCreate) -> Dict[str, Any]:
        """신규 데이터 생성 (Firestore 'data' 컬렉션)"""
        doc_id = f"data_{uuid.uuid4().hex[:8]}"
        data_dict = {
            "id": doc_id,
            "date": payload.date,
            "value": payload.value,
            "memo": payload.memo,
            "category": payload.category or "일반",
            "created_at": datetime.utcnow().isoformat()
        }

        if firebase_initialized and db:
            try:
                db.collection("data").document(doc_id).set(data_dict)
                logger.info(f"Firestore 데이터 생성 완료: {doc_id}")
            except Exception as e:
                logger.error(f"Firestore create_data 에러: {e}")

        # Fallback 스토리지에도 항상 반영
        _memory_data[doc_id] = data_dict
        return data_dict

    @staticmethod
    async def update_data(data_id: str, payload: DataUpdate) -> Optional[Dict[str, Any]]:
        """데이터 수정"""
        update_fields = {}
        if payload.date is not None:
            update_fields["date"] = payload.date
        if payload.value is not None:
            update_fields["value"] = payload.value
        if payload.memo is not None:
            update_fields["memo"] = payload.memo
        if payload.category is not None:
            update_fields["category"] = payload.category
        
        update_fields["updated_at"] = datetime.utcnow().isoformat()

        if firebase_initialized and db:
            try:
                doc_ref = db.collection("data").document(data_id)
                doc = doc_ref.get()
                if not doc.exists:
                    return None
                doc_ref.update(update_fields)
                updated_doc = doc_ref.get().to_dict()
                updated_doc["id"] = data_id
                _memory_data[data_id] = updated_doc
                return updated_doc
            except Exception as e:
                logger.error(f"Firestore update_data 에러: {e}")

        # Fallback
        if data_id in _memory_data:
            _memory_data[data_id].update(update_fields)
            return _memory_data[data_id]
        return None

    @staticmethod
    async def delete_data(data_id: str) -> bool:
        """데이터 삭제"""
        deleted = False
        if firebase_initialized and db:
            try:
                doc_ref = db.collection("data").document(data_id)
                doc = doc_ref.get()
                if doc.exists:
                    doc_ref.delete()
                    deleted = True
            except Exception as e:
                logger.error(f"Firestore delete_data 에러: {e}")

        if data_id in _memory_data:
            del _memory_data[data_id]
            deleted = True

        return deleted

    # -------------------------------------------------------------
    # 2. 대화 기록 (conversations 컬렉션) CRUD
    # -------------------------------------------------------------
    @staticmethod
    async def get_all_conversations() -> List[Dict[str, Any]]:
        """대화 목록 조회 (최신순)"""
        if firebase_initialized and db:
            try:
                direction = firestore.Query.DESCENDING if (firestore and hasattr(firestore, "Query")) else "DESCENDING"
                docs = db.collection("conversations").order_by("updated_at", direction=direction).stream()
                result = []
                for doc in docs:
                    d = doc.to_dict()
                    d["id"] = doc.id
                    d["message_count"] = len(d.get("messages", []))
                    result.append(d)
                return result
            except Exception as e:
                logger.error(f"Firestore get_all_conversations 에러: {e}")

        # Fallback
        convs = list(_memory_conversations.values())
        convs.sort(key=lambda x: x.get("updated_at", x.get("created_at", "")), reverse=True)
        for c in convs:
            c["message_count"] = len(c.get("messages", []))
        return convs

    @staticmethod
    async def get_conversation_by_id(conv_id: str) -> Optional[Dict[str, Any]]:
        """특정 대화 상세 조회 (전체 메시지 내역 포함)"""
        if firebase_initialized and db:
            try:
                doc = db.collection("conversations").document(conv_id).get()
                if doc.exists:
                    d = doc.to_dict()
                    d["id"] = doc.id
                    return d
                return None
            except Exception as e:
                logger.error(f"Firestore get_conversation_by_id 에러: {e}")

        # Fallback
        return _memory_conversations.get(conv_id)

    @staticmethod
    async def save_or_update_conversation(conv_id: Optional[str], title: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """대화 세션 저장 또는 메시지 추가 업데이트"""
        cid = conv_id if conv_id else f"conv_{uuid.uuid4().hex[:8]}"
        now_str = datetime.utcnow().isoformat()

        # 기존 대화 확인
        existing = await FirestoreService.get_conversation_by_id(cid)
        created_at = existing.get("created_at", now_str) if existing else now_str

        conv_dict = {
            "id": cid,
            "title": title or (messages[0].get("content", "새로운 대화")[:25] if messages else "새로운 대화"),
            "messages": messages,
            "created_at": created_at,
            "updated_at": now_str
        }

        if firebase_initialized and db:
            try:
                db.collection("conversations").document(cid).set(conv_dict)
                logger.info(f"Firestore 대화 저장 완료: {cid}")
            except Exception as e:
                logger.error(f"Firestore save_conversation 에러: {e}")

        # Fallback
        _memory_conversations[cid] = conv_dict
        return conv_dict

    @staticmethod
    async def delete_conversation(conv_id: str) -> bool:
        """대화 삭제"""
        deleted = False
        if firebase_initialized and db:
            try:
                doc_ref = db.collection("conversations").document(conv_id)
                if doc_ref.get().exists:
                    doc_ref.delete()
                    deleted = True
            except Exception as e:
                logger.error(f"Firestore delete_conversation 에러: {e}")

        if conv_id in _memory_conversations:
            del _memory_conversations[conv_id]
            deleted = True

        return deleted
