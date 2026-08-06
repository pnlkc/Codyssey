#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request


try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


def load_env_file(env_path=".env"):
    """
    .env 파일이 존재할 경우 환경 변수로 로드합니다.
    python-dotenv 패키지가 설치되어 있으면 사용하고, 없을 경우 자체 로더를 활용합니다.
    """
    candidates = [
        env_path,
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.getcwd(), "A1-2", "과제산출물", ".env")
    ]
    for path in candidates:
        if os.path.exists(path):
            if HAS_DOTENV:
                load_dotenv(path)
                return
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip("'").strip('"')
                        if key and key not in os.environ:
                            os.environ[key] = value


def validate_date(date_str):
    """
    YYYY-MM-DD 날짜 형식을 검증합니다.
    """
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_api_keys():
    """
    환경 변수에서 API 키를 읽어옵니다.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    kakao_key = os.environ.get("KAKAO_REST_API_KEY") or os.environ.get("KAKAO_API_KEY")
    return gemini_key, kakao_key


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
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            candidates = res_json.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return ""
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API HTTP Error {e.code}: {error_body}")
    except Exception as e:
        raise RuntimeError(f"Gemini API 호출 실패: {str(e)}")


def parse_json_response(text):
    """
    LLM 응답 텍스트에서 JSON 객체를 추출하여 파싱합니다.
    """
    text = text.strip()
    # 마크다운 코드블록 제거
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
            
    data = json.loads(text)
    required_keys = ["recommended_city", "weather", "events", "reason"]
    for k in required_keys:
        if k not in data:
            raise KeyError(f"필수 키 누락: {k}")
    return data


def generate_first_recommendation(date_str, gemini_key):
    """
    LLM API를 연동하여 1차 추천 JSON을 생성합니다. (실패 시 1회 재시도)
    """
    base_prompt = (
        f"사용자가 {date_str}에 국내 여행을 가려고 합니다.\n"
        f"이 날짜 시기에 어울리는 한국의 여행지 도시 1곳을 추천하고 일반적 날씨 요약, 주요 행사/축제 후보(1~3개), 추천 이유(2~4문장)를 작성해주세요.\n"
        f"반드시 마크다운이나 기타 다른 텍스트 없이 유효한 JSON 형식으로만 응답해야 합니다.\n"
        f"JSON 스키마 규격:\n"
        f"{{\n"
        f'  "recommended_city": "도시명 (예: 제주, 강릉, 경주)",\n'
        f'  "weather": "날씨 요약문",\n'
        f'  "events": ["행사1", "행사2"],\n'
        f'  "reason": "추천 근거 2~4문장"\n'
        f"}}\n"
    )
    
    print("[1/3] 1차 추천 생성 중(LLM)...")
    errors = []
    
    # 1차 시도
    try:
        raw_text = call_gemini_api(base_prompt, gemini_key)
        parsed_json = parse_json_response(raw_text)
        print(f"  - recommended_city: \"{parsed_json.get('recommended_city')}\"")
        return parsed_json, errors
    except Exception as e:
        err_msg = f"1차 JSON 파싱/호출 실패: {str(e)}"
        print(f"  - 경고: {err_msg}. 재시도 프롬프트로 1회 재시도합니다.")
        errors.append({"step": "first_recommendation_attempt_1", "type": "JSON_PARSE_ERROR", "message": err_msg})
    
    # 2차 재시도 (프롬프트 보정)
    retry_prompt = (
        f"이전에 요청한 JSON 응답이 올바르지 않았습니다. 반드시 아래 필수 키만 포함된 순수 JSON으로만 출력해주세요.\n"
        f"필수 키: recommended_city, weather, events, reason\n\n" + base_prompt
    )
    try:
        raw_text = call_gemini_api(retry_prompt, gemini_key)
        parsed_json = parse_json_response(raw_text)
        print(f"  - (재시도 성공) recommended_city: \"{parsed_json.get('recommended_city')}\"")
        return parsed_json, errors
    except Exception as e:
        err_msg = f"2차 JSON 파싱/호출 실패: {str(e)}"
        print(f"  - 오류: {err_msg}. 기본 fallback 추천 정보를 사용합니다.")
        errors.append({"step": "first_recommendation_attempt_2", "type": "JSON_PARSE_ERROR", "message": err_msg})
        
        fallback_data = {
            "recommended_city": "제주",
            "weather": f"{date_str} 시기의 일반적인 날씨 요약 정보",
            "events": ["지역 대표 문화 행사"],
            "reason": f"{date_str} 시기에 방문하기 좋은 추천 여행지입니다."
        }
        return fallback_data, errors


def search_places_kakao(city, kakao_key):
    """
    Kakao Local API를 호출하여 맛집 목록을 검색합니다.
    """
    print("[2/3] 맛집 검색 중(지도/장소 API)...")
    places = []
    errors = []
    
    if not kakao_key:
        print("  - 오류: KAKAO_REST_API_KEY 미설정. 맛집 정보 조회를 스킵합니다.")
        errors.append({"step": "place_search", "type": "AUTH_ERROR", "message": "KAKAO_REST_API_KEY 미설정"})
        return places, errors
        
    query = f"{city} 맛집"
    encoded_query = urllib.parse.quote(query)
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={encoded_query}&size=5&category_group_code=FD6"
    headers = {
        "Authorization": f"KakaoAK {kakao_key}"
    }
    
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            documents = res_json.get("documents", [])
            
            if not documents:
                print("  - 검색 결과 0건 (다음 단계로 진행)")
                errors.append({"step": "place_search", "type": "EMPTY_RESULT", "message": f"0 results for query={query}"})
                return places, errors
                
            for doc in documents:
                places.append({
                    "name": doc.get("place_name", ""),
                    "address": doc.get("road_address_name") or doc.get("address_name", ""),
                    "category": doc.get("category_name", ""),
                    "url": doc.get("place_url", ""),
                    "x": doc.get("x", ""),
                    "y": doc.get("y", "")
                })
            print(f"  - 맛집 {len(places)}곳 검색 완료")
            return places, errors
            
    except urllib.error.HTTPError as e:
        err_msg = f"HTTP {e.code}"
        if e.code in (401, 403):
            print(f"  - 오류: 인증 실패({e.code}). Kakao API 키 설정을 확인하세요.")
            errors.append({"step": "place_search", "type": "AUTH_ERROR", "message": err_msg})
        else:
            print(f"  - 오류: 지도/장소 API 호출 실패({err_msg}).")
            errors.append({"step": "place_search", "type": "API_ERROR", "message": err_msg})
        print("  - 맛집 섹션은 '데이터 없음'으로 처리하고 계속 진행합니다.")
        return places, errors
    except Exception as e:
        err_msg = str(e)
        print(f"  - 오류: 맛집 검색 예외 발생 ({err_msg}). 맛집 섹션은 '데이터 없음' 처리합니다.")
        errors.append({"step": "place_search", "type": "NETWORK_ERROR", "message": err_msg})
        return places, errors


def generate_final_markdown_report(date_str, recommendation, places, errors, gemini_key):
    """
    LLM API를 활용하여 최종 Markdown 여행 리포트를 생성합니다.
    """
    print("[3/3] 최종 리포트 생성 중(LLM)...")
    
    prompt = (
        f"다음 여행 정보 데이터를 바탕으로 풍부하고 읽기 쉬운 Markdown 여행 리포트를 작성해 주세요.\n\n"
        f"여행 날짜: {date_str}\n"
        f"추천 지역: {recommendation.get('recommended_city')}\n"
        f"날씨 요약: {recommendation.get('weather')}\n"
        f"행사/축제: {', '.join(recommendation.get('events', []))}\n"
        f"추천 이유: {recommendation.get('reason')}\n"
        f"맛집 목록 데이터: {json.dumps(places, ensure_ascii=False)}\n\n"
        f"리포트는 반드시 아래 마크다운 헤더 구조를 포함해야 합니다:\n"
        f"# {date_str} 국내 여행 추천 리포트\n"
        f"## 추천 지역\n"
        f"## 추천 이유\n"
        f"## 날씨 요약\n"
        f"## 행사/축제\n"
        f"## 맛집 추천\n"
        f"(맛집 목록 데이터가 없거나 0건이면 반드시 '- 데이터 없음 (장소 검색 결과 0건)' 으로 표기해 주세요. 데이터가 있으면 이름, 주소, 카테고리, 링크 등을 깔끔하게 목록화해 주세요.)\n"
        f"## 1일 일정 제안\n"
        f"(오전/오후/저녁 나누어 제안)\n"
    )
    
    try:
        report_md = call_gemini_api(prompt, gemini_key)
        if report_md:
            print("  - 리포트 생성 완료")
            return report_md
    except Exception as e:
        print(f"  - 경고: 최종 리포트 LLM 생성 실패 ({str(e)}). 기본 템플릿으로 리포트를 작성합니다.")
        errors.append({"step": "final_report_generation", "type": "LLM_ERROR", "message": str(e)})

    # Fallback Markdown 작성
    events_str = "\n".join([f"- {e}" for e in recommendation.get("events", [])]) or "- 정보 없음"
    if places:
        places_str = "\n".join([f"- **{p['name']}** ({p.get('category','')}) - {p['address']} [상세보기]({p.get('url','')})" for p in places])
    else:
        places_str = "- 데이터 없음 (장소 검색 결과 0건)"
        
    fallback_md = f"""# {date_str} 국내 여행 추천 리포트

## 추천 지역
{recommendation.get('recommended_city')}

## 추천 이유
{recommendation.get('reason')}

## 날씨 요약
{recommendation.get('weather')}

## 행사/축제
{events_str}

## 맛집 추천
{places_str}

## 1일 일정 제안
- **오전**: {recommendation.get('recommended_city')} 도착 및 주요 관광지 둘러보기
- **오후**: 지역 대표 맛집 탐방 및 문화 행사/축제 관람
- **저녁**: 산책 및 여행 일과 마무리

"""
    return fallback_md


def save_results(date_str, recommendation, places, errors, markdown_content):
    """
    results/ 디렉토리에 원본 JSON 및 최종 Markdown 리포트를 저장합니다.
    """
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, f"{date_str}_travel_plan_raw.json")
    md_path = os.path.join(results_dir, f"{date_str}_travel_plan.md")
    
    raw_data = {
        "recommendation": recommendation,
        "places": places,
        "errors": errors
    }
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
        
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"\n완료! {md_path} 및 {json_path} 를 확인하세요.")


def main():
    load_env_file()
    
    parser = argparse.ArgumentParser(
        description="LLM과 지도 API를 활용한 CLI 국내 여행지 추천 및 리포트 생성 프로그램",
        usage="python main.py -date YYYY-MM-DD"
    )
    parser.add_argument(
        "-date",
        type=str,
        required=True,
        help="여행 날짜 (형식: YYYY-MM-DD, 예: -date \"2026-03-15\")"
    )
    
    args = parser.parse_args()
    date_str = args.date
    
    if not validate_date(date_str):
        print(f"오류: '{date_str}'는 올바른 날짜 형식이 아닙니다. (YYYY-MM-DD 형식 필요)")
        parser.print_help()
        sys.exit(1)
        
    gemini_key, kakao_key = get_api_keys()
    
    if not gemini_key:
        print("\n[오류] GEMINI_API_KEY 가 설정되지 않았습니다.")
        print("API 키 설정 방법:")
        print(" 1) .env 파일에 GEMINI_API_KEY=your_key 작성")
        print(" 2) 또는 터미널 환경 변수 설정 (PowerShell: $env:GEMINI_API_KEY=\"your_key\")")
        print(" 3) 지도 API 사용을 위해 KAKAO_REST_API_KEY 도 함께 설정해주세요.\n")
        sys.exit(1)
        
    all_errors = []
    
    # 1. LLM 1차 추천
    recommendation, rec_errors = generate_first_recommendation(date_str, gemini_key)
    all_errors.extend(rec_errors)
    
    # 2. 지도 API 맛집 검색
    city = recommendation.get("recommended_city", "제주")
    places, search_errors = search_places_kakao(city, kakao_key)
    all_errors.extend(search_errors)
    
    # 3. LLM 최종 리포트 작성
    report_md = generate_final_markdown_report(date_str, recommendation, places, all_errors, gemini_key)
    
    # 4. 결과 저장
    save_results(date_str, recommendation, places, all_errors, report_md)


if __name__ == "__main__":
    main()
