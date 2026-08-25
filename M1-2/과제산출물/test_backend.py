"""
FastAPI Backend Integration Test Suite
모든 핵심 엔드포인트(Data CRUD + Summary + Conversations + Chat + Health) 검증
"""
import sys
import io

# 콘솔 UTF-8 출력 강제 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_all():
    print(">> [통합 테스트] FastAPI 백엔드 엔드포인트 전수 테스트 시작...")

    # 1. Health Check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] 1. GET /api/health 통과")

    # 2. Data Summary
    res = client.get("/api/data/summary")
    assert res.status_code == 200, f"Summary failed: {res.text}"
    summary = res.json()
    assert summary["count"] >= 100, f"Expected at least 100 records, got {summary['count']}"
    assert "metrics" in summary
    assert "trend" in summary
    print(f"[PASS] 2. GET /api/data/summary 통과 (레코드 수: {summary['count']}개, 평균: {summary['metrics']['average']})")

    # 3. Data CRUD
    # 3-1. Create
    new_item = {
        "date": "2026-03-01",
        "value": 999.0,
        "memo": "자동화 테스트 데이터",
        "category": "테스트"
    }
    res = client.post("/api/data", json=new_item)
    assert res.status_code == 201, f"Create failed: {res.text}"
    created = res.json()
    item_id = created["id"]
    print(f"[PASS] 3-1. POST /api/data 통과 (생성 ID: {item_id})")

    # 3-2. Read List
    res = client.get("/api/data?limit=5")
    assert res.status_code == 200
    assert len(res.json()) <= 5
    print("[PASS] 3-2. GET /api/data (목록 조회) 통과")

    # 3-3. Read Single
    res = client.get(f"/api/data/{item_id}")
    assert res.status_code == 200
    assert res.json()["value"] == 999.0
    print("[PASS] 3-3. GET /api/data/{id} (단건 조회) 통과")

    # 3-4. Update
    res = client.put(f"/api/data/{item_id}", json={"value": 1050.0, "memo": "테스트 데이터 수정"})
    assert res.status_code == 200
    assert res.json()["value"] == 1050.0
    print("[PASS] 3-4. PUT /api/data/{id} (수정) 통과")

    # 3-5. Delete
    res = client.delete(f"/api/data/{item_id}")
    assert res.status_code == 200
    print("[PASS] 3-5. DELETE /api/data/{id} (삭제) 통과")

    # 4. Conversations API
    # 4-1. Create Conversation
    conv_payload = {
        "title": "테스트 대화 세션",
        "messages": [
            {"role": "user", "content": "안녕하세요"},
            {"role": "assistant", "content": "네 반갑습니다!"}
        ]
    }
    res = client.post("/api/conversations", json=conv_payload)
    assert res.status_code == 201
    conv_id = res.json()["id"]
    print(f"[PASS] 4-1. POST /api/conversations (대화 생성) 통과 (ID: {conv_id})")

    # 4-2. List Conversations
    res = client.get("/api/conversations")
    assert res.status_code == 200
    assert len(res.json()) >= 1
    print("[PASS] 4-2. GET /api/conversations (대화 목록) 통과")

    # 4-3. Get Single Conversation (대화 불러오기)
    res = client.get(f"/api/conversations/{conv_id}")
    assert res.status_code == 200
    assert len(res.json()["messages"]) == 2
    print("[PASS] 4-3. GET /api/conversations/{id} (대화 불러오기) 통과")

    # 4-4. Delete Conversation
    res = client.delete(f"/api/conversations/{conv_id}")
    assert res.status_code == 200
    print("[PASS] 4-4. DELETE /api/conversations/{id} (대화 삭제) 통과")

    # 5. AI Chat API (컨텍스트 주입 및 자동 저장)
    chat_payload = {
        "message": "이번 달 실적과 최근 트렌드가 어때?"
    }
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200
    chat_res = res.json()
    assert "reply" in chat_res
    assert "conversation_id" in chat_res
    assert chat_res["summary_applied"] is not None
    print(f"[PASS] 5. POST /api/chat (컨텍스트 주입 AI 대화) 통과 (응답 모델: {chat_res['model_used']})")

    print("\n[SUCCESS] 모든 백엔드 엔드포인트 통합 검증을 100% 성공적으로 통과했습니다!")

if __name__ == "__main__":
    test_all()
