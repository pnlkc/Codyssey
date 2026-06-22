# Changelog

모든 변경 이력은 이 파일에 기록됩니다.

## [1.0.0/2026-06-17] - [👔 Project Manager]
- **작업 내용:** 퍼실리테이터 역량 강화 발표용 `facilitator_guide.md` 문서 작성 및 프로젝트 워크스페이스 배치.
- **사유:** 비전공자/왕초보 교육생을 효과적으로 지도하기 위해 30분 세션 구조와 쉬운 한국어 개념 번역, 현장 상황극 시나리오, Sora2 화질 질문 등 돌발상황 대처법을 포함한 지침서 작성.
- **최종 개편:** 발표 현장에서 파일 화면을 띄워두고 바로 활용할 수 있도록 Marp 프레젠테이션 설정값, 슬라이드 구분자, 그리고 모든 외부 하이퍼링크(URL)를 완전히 걷어내고 정돈된 일반 마크다운(Pure Markdown) 문서 형식으로 변환 완료.
- **AI 네이티브 목표 지향 개편 (최종):** 단순 마케팅 기획 이론(USP 등)이나 영상 인코딩 스펙(mp4, 코덱)에 대한 해설 집착을 걷어내고, 멀티모달 도구별 장단점 파악, 프롬프트를 통한 AI 제어력 훈련, Google Flow 에러 대응 등 실제 AI 제어 및 파이프라인 조립력 향상이라는 교육 목표 위주로 전체 콘텐츠 재구조화 완료.
- **세부 개정:** 교육생에게 꼭 필요한 핵심 기술 용어인 cref, sref, ControlNet의 구두 가이드 부분을 직관적인 일상 언어(도장, 스티커, 가이드선) 비유로 보강 완료.
- **맥OS(macOS) 최적화 및 텍스트 슬림화:** 조잡한 기계적 단축키 나열을 걷어내고, 맥 환경 기준(Command + C/V, Finder 내 단축키 Cmd+Opt+L, 초록색 확대 버튼을 통한 화면 Split View 분할법 등)의 퍼실리테이터 행동 카드 배포 및 사전 스냅 가이드와 같은 거시적 보조 프레임워크로 깔끔하게 정돈 완료.
- **리터러시 및 템플릿 보강 개정:** 컴퓨터 사용 자체가 서툰 완전 생초보 교육생들이 겪는 실질적인 기초 조작 장벽(소셜 로그인 팝업 오류, 복사/붙여넣기 단축키 서툼, 다운로드 파일 위치 유실, PDF 내보내기 방법 곤란)에 대한 퍼실리테이터의 2차 세부 수칙 및 가상 브랜드 템플릿 3종 예시를 사전 공급하여 5분 내로 기획을 마치는 파이프라인 정체 돌파 전략 보강 완료.
- **작업 내용:** 교육생 예상 질문 및 난관 정리서 `learning_qa_and_bottlenecks.md` 파일 신규 생성.
- **사유:** 복잡한 가이드북 형식 대신 발표 화면에 직관적으로 띄워 사용할 수 있는 Q&A 중심의 문서 요청에 부합하도록 맥OS 기초 장벽, 유료 툴 대안, Sora2 화질 질문 및 Runway 프롬프트 한계 대책을 리스트화하여 구성.
- **근본 개정 (최종):** 외부 툴 지식(Gemini, Vrew, Flow, Stable Diffusion 등)과 실습 로그를 완전히 배제하고, 오직 B1-2 명세서 텍스트 자체(파이프라인, 멀티모달, cref/sref, ControlNet, 코덱 규격 등)만을 읽고 AI 생초보 교육생이 느낄 만한 인지적 당혹감과 병목 사항 위주의 '순수한 15대 예상 질문 및 난관 리스트'로 최종 교정 및 정돈 완료.
- **작업 내용:** 프로젝트 내 복제본 `facilitator_guide.md` 파일 영구 삭제(DELETE).
- **사유:** 사용자의 '근본 복구' 요청에 따라 워크스페이스 내에 생성되었던 발표 가이드 문서를 정리하고 프로젝트 클린 상태 유지.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 검증 완료 (통과).

## [1.1.0/2026-06-17] - [👔 Project Manager]
- **작업 내용:** `learning_qa_and_bottlenecks.md` 내 생초보 예상 Q&A를 55선에서 135선으로 대폭 확장 및 보완.
- **사유:** 사용자의 추가 질문 무제한 추출 요청에 부합하도록, B1-2 명세서 원문의 모든 조항(분야, 구분, 미션, 결과물, 코덱, 보너스, 제약사항, 결과 예시)을 한 줄씩 현미경으로 관찰하여 AI 생초보가 가질 법한 직관적이고 세부적인 질문과 난관을 135개로 전수 상세화함.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js`를 실행하여 정적 및 구문 검증 완료.

## [1.2.0/2026-06-18] - [👔 Project Manager]
- **작업 내용:** `learning_qa_and_bottlenecks.md` 내 예상 질문 135선에 대한 퍼실리테이터 답변 예시 전수 작성 및 수록 완료.
- **사유:** 사용자의 요청에 부합하도록, 비전공자 생초보 학습자들의 눈높이에 맞춘 직관적인 비유와 명세서 정량/정성 제약 조건 기반의 실전 답변 예시를 135개 전체 문항에 개별 매핑함.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js`를 실행하여 정적 및 구문 검증 완료.

## [1.3.0/2026-06-18] - [👔 Project Manager]
- **작업 내용:** 
  - 기존 B1-2 Q&A 파일 `learning_qa_and_bottlenecks.md`를 `learning_qa_and_bottlenecks_b1_2.md`로 파일명 변경 완료.
  - B1-3 명세서 원문을 현미경 분석하여 노코드 업무 자동화(Make, Zapier) 관련 생초보 Q&A 및 답변 예시 100선이 수록된 `learning_qa_and_bottlenecks_b1_3.md` 파일 신규 생성 완료.
- **사유:** 사용자의 추가 명세서(B1-3) Q&A 추출 및 파일 구분 요구에 정합적으로 대응하기 위함.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js`를 실행하여 정적 및 구문 검증 완료.

## [1.4.0/2026-06-18] - [👔 Project Manager]
- **작업 내용:** 
  - 명세서 및 Q&A 파일들의 명칭을 사용자의 요청에 따라 표준 규칙으로 변경 완료.
    - `B1-2 명세서.md` -> `B1-2_명세서.md`
    - `B1-3 명세서.md` -> `B1-3_명세서.md`
    - `learning_qa_and_bottlenecks_b1_2.md` -> `B1-2_Q&A.md`
    - `learning_qa_and_bottlenecks_b1_3.md` -> `B1-3_Q&A.md`
- **사유:** 파일명 표준화 및 가독성 향상.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js`를 실행하여 정적 및 구문 검증 완료.

## [1.5.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - B1-1 명세서 기반 예상 질문 100선 및 답변 예시가 포함된 `B1-1_Q&A.md` 파일 생성.
  - 교육생들의 이해도와 학습 상황을 파악할 수 있는 확인 질문과 피드백용 개입 가이드가 담긴 `B1-1_체크리스트.md` 신규 파일 작성.
  - 사용자의 피드백에 대응하여 `B1-1_체크리스트.md` 내 체크 포인트를 40선으로 대폭 확장하고 각 항목별 개별 참고 레퍼런스 란 및 문서 최하단 통합 학습 레퍼런스 영역 신규 배치 완료.
  - Q&A와 체크리스트를 결합하여 명세서 흐름에 따른 퍼실리테이터 전용 통합 지도 문서인 `B1-1_통합가이드.md` 파일 신규 작성.
  - 사용자의 요청에 따라 `B1-1_통합가이드.md` 내의 '퍼실리테이터의 이해도 체크' 표제어를 '이해도 체크'로 일괄 변경 및 표준화 완료.
- **사유:** 사용자 편의성 향상 및 챗봇 설계 가이드 문서 표제어 레이아웃의 간결화 및 일관성 확보.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 검증 완료 (통과).

## [1.6.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - `B1-1_체크리스트.md` 및 `B1-1_통합가이드.md` 내 참고 레퍼런스 영역에 실제 정상 접속 가능하며 5대 요건(접속 보장, 한글화, 내용 일치, 비전공자 가독성, 필요한 사전지식 명시)을 충족하는 신뢰성 높은 링크(Cloudflare, 네이버 지식백과, Azure OpenAI 공식 기술 문서) 매핑 완료.
  - 최하단 '🔗 통합 학습 레퍼런스'에 Microsoft Learn 공식 프롬프트 가이드를 추가 보강하여 전체 자료 완성도 향상.
- **사유:** 사용자의 교육생용 한글 레퍼런스 기준 준수 및 참고 링크 고도화 요청 반영.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.7.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - 사용자가 `B1-1_통합가이드.md`에서 직접 개정한 참고 레퍼런스(브런치, 위키독스, 코드트리, 요즘IT 등) 및 피드백 개입 가이드 수정본을 `B1-1_체크리스트.md`로 100% 동방향 자동 동기화(Sync) 완료.
  - 최하단 '🔗 통합 학습 레퍼런스' 영역을 본문에서 사용된 링크들만 한정 표기하도록 정비하여 최종 8종의 핵심 한글 레퍼런스 체계로 동기화 갱신 완료.
- **사유:** 사용자의 수동 편집 내용에 대응한 두 보조 지도 자료 간의 기획 정합성 및 동기화 무결성 확보.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.8.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - [B1-1_통합가이드.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_통합가이드.md) 및 [B1-1_Q&A.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_Q&A.md) 파일 내 모든 Q&A 단락에 기재되어 있던 `* **나의 답변**: [여기에 내가 생각하는 답변을 적어주세요]` 플레이스홀더 라인을 일괄 영구 삭제 완료.
- **사유:** 사용자의 직접 답변 입력 및 교정 용의를 돕기 위한 보조 지문 제거 및 문서 슬림화.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.9.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - `B1-1_체크리스트.md`, `B1-1_통합가이드.md`, `B1-1_Q&A.md` 3개 문서 내의 `Temperature` 및 `Top_p` 파라미터 확인 질문과 답변의 비유(상상력 온도 다이얼, 얌전함 다이얼)를 초보자 눈높이에 맞게 보강 갱신 완료.
  - 질문 문항 속 비격식적 호칭인 '비전공자 친구' 표현을 공식적이고 전문적인 '인공지능을 처음 접하는 동료'로 일제 교정 완료.
- **사유:** 피드백 반영을 통한 교육용 보조 지도 가이드로서의 격식 및 용어 직관성 확보.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.10.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - [B1-1_통합가이드.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_통합가이드.md) 내에서 중복 기재되어 있던 두 번째 `[영역 3]`을 `[영역 4]`로 시프트 교정하고, 그 이하의 모든 영역 번호(총 33개)를 순차적으로 1씩 올려 정상 인덱스로 일제 정규화 완료.
- **사유:** 영역 인덱스 중복 기재 오류 보정 및 교재로서의 일련성 정합성 확보.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.11.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - [B1-1_통합가이드.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_통합가이드.md)와 [B1-1_체크리스트.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_체크리스트.md) 내에서 명세서 기준인 `5. 보너스 과제`, `6. 제약 사항`, `7. 결과 예시` 단락을 독자적인 대분류 헤더(##)로 완전히 분리 정비 완료.
  - 가이드 및 체크리스트의 구조를 1~42 항목 체계로 일관되게 정규화하였으며, 누락되었던 파이프라인 개념, 사용 환경 재현성, 10턴 펜스 유지, 보너스 GPTs 배포 방식, 결과 예시 검토 항목을 상호 1:1 동치로 동기화 수록 완료.
- **사유:** 명세서 구조 흐름과의 완전한 매칭을 도모하고, 퍼실리테이터의 양대 지도 자료 점검 정합성을 극대화하기 위함.
- **사유:** 명세서 구조 흐름과의 완전한 매칭을 도모하고, 퍼실리테이터의 양대 지도 자료 점검 정합성을 극대화하기 위함.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.11.1/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - [B1-1_통합가이드.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_통합가이드.md)와 [B1-1_체크리스트.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_체크리스트.md) 내 42개 영역에 포함된 '퍼실리테이터 개입 가이드'의 어조를 직접 답을 지시하는 형태에서 질문과 힌트를 제시하는 "유도형 질문"으로 개정 및 1:1 동기화 완료.
  - 이전 동기화 과정에서 꼬여서 중복으로 복사되어 들어갔던 영역 12번~42번의 세부 속성 데이터(확인 질문, 자가진단 난관 지표, 통과 기준, Q&A 등)를 명세서 사양에 맞게 각각 고유하고 올바른 독립 팩트로 완전 복원 완료.
- **사유:** 사용자의 개입 가이드 유도형 개선 요청을 반영하고, 문서 간의 정량적 정합성과 기획 무결성을 동시에 완성하기 위함.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 및 `memory_manager.js` 전역 하네스 자가 검증 통과(Exit Code 0).

## [1.12.0/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - `B1-1_명세서.md` 및 `B1-1_체크리스트.md` 2개 파일을 워크스페이스 내에서 영구 삭제(DELETE).
- **사유:** `B1-1_통합가이드.md` 문서 내에 명세서 조건 및 체크리스트의 모든 평가 항목이 1:1로 수록 완료되어 개별 파일 유지의 필요성이 사라짐에 따른 최종 파일 정비.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.12.1/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - [B1-1_통합가이드.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_통합가이드.md) 내에 빈 플레이스홀더로 남아 있던 `* **참고 레퍼런스**: [추가 학습 시 참고할 참고 자료 링크를 적어주세요]` 라인을 일괄 영구 삭제 완료.
- **사유:** 참조할 링크가 아직 부재한 영역들에 불필요한 공란 플레이스홀더 라인을 유지하지 않고 제거하여 문서 가독성과 미적 정돈도를 향상시키기 위함.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 및 `memory_manager.js` 전역 하네스 자가 검증 통과(Exit Code 0).

## [1.12.2/2026-06-19] - [👔 Project Manager]
- **작업 내용:** 
  - [B1-1_통합가이드.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_통합가이드.md) 내의 영역 구분 타이틀 번호 표기를 기존 `[영역 1]` 형태에서 `[1]` 형태로 전면 간소화 일괄 교정 완료.
- **사유:** 불필요하게 반복되는 '영역' 어휘를 걷어내고 가장 간결한 숫자 대괄호 번호판으로 미니멀리즘 포맷 디자인을 완성하기 위함.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 및 `memory_manager.js` 전역 하네스 자가 검증 통과(Exit Code 0).

## [1.13.0/2026-06-22] - [👔 Project Manager]
- **작업 내용:** [B1-1_통합가이드.md](file:///c:/Users/pnlkc/AIProject/Codyssey/B1-1/B1-1_통합가이드.md) 내 '퍼실리테이터 개입 가이드' 항목(총 42개 영역)의 어조를 기존 청유/권유형(~하세요)에서 명확한 지시/가이드형(~한다) 종결형으로 일괄 교정 및 수정 완료. 398번 영역의 누락된 닫는 따옴표 오류 보정.
- **사유:** 사용자의 개입 가이드 종결 어미 일괄 지시 가이드 문구화 요청 반영.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료 (통과).

## [1.14.0/2026-06-22] - [👔 Project Manager]
- **작업 내용:** B1-3 명세서 및 Q&A 기반 퍼실리테이터 통합 지도서 `B1-3_통합가이드.md` 신규 작성 및 기존 `B1-2_Q&A.md`, `B1-3_Q&A.md` 파일 영구 삭제.
- **사유:** 사용자의 추가 가이드 통합 및 개별 Q&A 파일 삭제 요청에 따른 파일 구조 최적화 및 문서 일괄 가이드화 반영. '퍼실리테이터 개입 가이드' 문구를 `~한다` 지시형 종결 어미로 통일.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료.

## [1.15.0/2026-06-22] - [👔 Project Manager]
- **작업 내용:** 레거시 Q&A 개별 파일 정리의 일환으로 `B1-1_Q&A.md` 파일 영구 삭제.
- **사유:** `B1-1_통합가이드.md` 문서 내에 `B1-1_Q&A.md` 내용이 100% 통합 수록되어 있어 개별 파일 유지의 필요성이 사라짐에 따른 최종 파일 정비.
- **검증 결과:** `node C:\Users\pnlkc\.gemini\config\plugins\antigravity-harness-plugin\scripts\verify.js` 정적 구문 및 테스트 검증 완료.

