#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler


def load_env():
    """
    .env 파일에서 환경변수를 로드합니다. (python-dotenv 우선 지원)
    """
    candidates = [
        ".env",
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.getcwd(), "A1-3", "과제산출물", ".env"),
        os.path.join(os.getcwd(), ".env")
    ]
    
    try:
        from dotenv import load_dotenv
        for path in candidates:
            if os.path.exists(path):
                load_dotenv(path)
    except ImportError:
        pass

    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'").strip('"')
                        if k and k not in os.environ:
                            os.environ[k] = v


def call_gemini_api(prompt, api_key):
    """
    Google Gemini REST API (gemini-3.5-flash-lite)를 호출합니다.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    with urllib.request.urlopen(req, timeout=25) as response:
        res_body = response.read().decode("utf-8")
        res_json = json.loads(res_body)
        candidates = res_json.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
        return ""


def parse_json_from_llm(text):
    """
    LLM 응답에서 JSON 객체를 추출하여 파싱합니다.
    """
    text = text.strip()
    if "```" in text:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            text = match.group(1)
        else:
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and start < end:
                text = text[start:end+1]
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and start < end:
            text = text[start:end+1]

    return json.loads(text)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """CORS Preflight 응답"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        load_env()
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

        if not api_key:
            self._send_json(
                {"error": "서버 환경변수(GEMINI_API_KEY)가 설정되지 않았습니다."},
                status=500
            )
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""

        try:
            req_data = json.loads(body) if body else {}
        except Exception:
            self._send_json({"error": "유효하지 않은 요청 JSON 포맷입니다."}, status=400)
            return

        keyword = req_data.get("keyword", "").strip()
        level = req_data.get("level", "중급 (핵심 개념 & 특징)").strip()

        if not keyword:
            self._send_json({"error": "학습할 키워드를 입력해 주세요."}, status=400)
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

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
