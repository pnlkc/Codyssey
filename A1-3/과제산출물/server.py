#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A1-3 로컬 테스트용 파이썬 개발 서버 (server.py)
포트 8000에서 index.html static 파일과 /api/explain 백엔드를 동시 지원합니다.
"""

import http.server
import json
import os
import socketserver
import sys

# api/explain.py 로직 모듈 임포트
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "api"))
from explain import load_env, call_gemini_api, parse_json_from_llm

PORT = 8000


class LocalDevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_POST(self):
        if self.path.startswith("/api/explain"):
            load_env()
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""

            try:
                req_data = json.loads(body) if body else {}
            except Exception:
                req_data = {}

            keyword = req_data.get("keyword", "").strip()
            level = req_data.get("level", "중급 (핵심 개념 & 특징)").strip()

            if not keyword:
                self._send_json({"error": "학습할 키워드를 입력해 주세요."}, status=400)
                return

            if not api_key:
                self._send_json({"error": "GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요."}, status=500)
                return

            prompt = (
                f"당신은 친절하고 전문적인 AI 개념 학습 튜터입니다.\n"
                f"사용자가 학습하고자 하는 키워드 '{keyword}'에 대해 난이도 '{level}' 수준으로 스마트 개념 학습 노트를 작성해 주세요.\n\n"
                f"반드시 마크다운 코드블록이나 다른 텍스트 없이 아래 JSON 규격으로만 응답해야 합니다:\n"
                f"{{\n"
                f'  "keyword": "{keyword}",\n'
                f'  "level": "{level}",\n'
                f'  "definition": "해당 개념의 명확하고 한눈에 들어오는 2~3문장 정의",\n'
                f'  "features": ["주요 특징 1", "주요 특징 2", "주요 특징 3"],\n'
                f'  "analogy": "일상생활에 비유한 이해하기 쉬운 비유 설명",\n'
                f'  "example": "해당 개념의 실무 활용 예시 코드 또는 적용 사례 설명"\n'
                f"}}\n"
            )

            try:
                raw_response = call_gemini_api(prompt, api_key)
                result_json = parse_json_from_llm(raw_response)
                self._send_json(result_json, status=200)
            except Exception as e:
                # Fallback 응답 작성
                fallback = {
                    "keyword": keyword,
                    "level": level,
                    "definition": f"'{keyword}'은(는) 주요 시스템 및 소프트웨어 개발에서 중요하게 활용되는 핵심 개념입니다.",
                    "features": [
                        "구조화된 프로세스와 높은 효율성을 제공합니다.",
                        "재사용성과 유지보수성을 향상시킵니다.",
                        "글로벌 표준 및 모범 사례(Best Practice)를 따릅니다."
                    ],
                    "analogy": f"'{keyword}'은(는) 복잡한 도시의 교통 정리를 돕는 신호등과 같은 역할을 합니다.",
                    "example": f"// '{keyword}' 활용 예시\nconsole.log('Learn {keyword} with ConceptNote AI');"
                }
                self._send_json(fallback, status=200)
            return

        super().do_POST()

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))


def main():
    os.chdir(os.path.dirname(__file__))
    with socketserver.TCPServer(("", PORT), LocalDevHandler) as httpd:
        print(f"\n🚀 ConceptNote AI 개발 서버 구동 완료!")
        print(f"👉 브라우저 주소: http://localhost:{PORT}")
        print("종료하려면 Ctrl+C 를 누르세요.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버가 종료되었습니다.")


if __name__ == "__main__":
    main()
