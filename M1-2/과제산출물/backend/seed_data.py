import os
import json
import logging
from config import db, firebase_initialized

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_data")

SAMPLE_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "sample_timeseries.json")

def run_seed():
    """120개의 시계열 샘플 데이터를 Firestore에 일괄 등록"""
    if not os.path.exists(SAMPLE_DATA_FILE):
        logger.error(f"샘플 데이터 파일을 찾을 수 없습니다: {SAMPLE_DATA_FILE}")
        return

    with open(SAMPLE_DATA_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)

    logger.info(f"총 {len(items)}개의 샘플 데이터를 로드했습니다.")

    if not firebase_initialized or not db:
        logger.warning("Firebase Firestore가 초기화되지 않았습니다. (.env 설정 확인 필요)")
        logger.info("로컬 Fallback 모드에서는 sample_timeseries.json 파일이 자동으로 사용됩니다.")
        return

    logger.info("Firestore 'data' 컬렉션의 기존 데이터를 정리하고 새 데이터 시딩을 시작합니다...")
    
    # 1. 기존 문서 삭제
    existing_docs = db.collection("data").stream()
    del_batch = db.batch()
    del_count = 0
    for doc in existing_docs:
        del_batch.delete(doc.reference)
        del_count += 1
        if del_count % 400 == 0:
            del_batch.commit()
            del_batch = db.batch()
    del_batch.commit()
    logger.info(f"기존 Firestore 데이터 {del_count}개 삭제 완료")

    # 2. 신규 데이터 일괄 등록
    batch = db.batch()
    batch_count = 0
    total_written = 0

    for item in items:
        doc_id = item.get("id")
        doc_ref = db.collection("data").document(doc_id)
        batch.set(doc_ref, item)
        batch_count += 1
        total_written += 1

        if batch_count >= 400:
            batch.commit()
            logger.info(f"중간 커밋: {total_written}개 완료")
            batch = db.batch()
            batch_count = 0

    if batch_count > 0:
        batch.commit()

    logger.info(f"🎉 성공: 총 {total_written}개의 시계열 데이터가 Firestore에 정상 시딩되었습니다!")

if __name__ == "__main__":
    run_seed()
