# 전역 변수
category_map = {
    1: "텍스트 생성",
    2: "이미지 생성",
    3: "영상 생성",
    4: "페르소나",
    5: "자동화",
    6: "기타"
}
# Prompt 클래스
class Prompt:
    def __init__(self, title: str, content: str, category: int, favorite: bool = False):
        self.title = title
        self.content = content
        self.category = category
        self.favorite = favorite


prompts = [
    Prompt('블로그 글 작성 도우미', '당신은 10년 경력의 전문 블로거입니다.', 1, True),
    Prompt('고양이 사진 생성기', '당신은 고양이 사진 전문가입니다.', 2, False),
    Prompt('영상 제작 도우미', '당신은 영상 제작 전문가입니다.', 3, False),
    Prompt('AI 챗봇', '당신은 AI 챗봇입니다.', 4, False),
    Prompt('자동화 프로그램', '당신은 자동화 프로그램입니다.', 5, False),
    Prompt('점심 메뉴 추천기', '당신은 점심 메뉴 추천 전문가입니다.', 6, False),
]


# 메인 메뉴
def main_menu() -> int:
    print(
        """
=== 나만의 프롬프트 관리 ===
1. 프롬프트 추가
2. 프롬프트 목록
3. 카테고리별 조회
4. 프롬프트 검색
5. 프롬프트 상세 보기
6. 즐겨찾기 관리
7. 즐겨찾기 목록
0. 종료
"""
    )

    print('선택: ', end='')
    select = input()
    
    if not select.isdigit() or int(select) < 0 or int(select) > 7:
        print("""
#########################################
0~7 사이의 숫자를 입력해주세요.
#########################################
""")
        return -1
    else:
        return int(select)


# 1. 프롬프트 추가
def add_prompt():
    print('=== 프롬프트 추가 ===')
    print('제목: ', end='')
    title = input()

    print('내용: ', end='')
    content = input()

    print("""
카테고리 선택:
1) 텍스트 생성
2) 이미지 생성
3) 영상 생성
4) 페르소나
5) 자동화
6) 기타
선택: """, end='')
    select = input()

    if not select.isdigit() or int(select) < 1 or int(select) > 6:
        print("########################################")
        print("1~6 사이의 숫자를 입력해주세요.")
        print("########################################")
        return

    category = int(select)

    newPrompt = Prompt(title, content, category)
    prompts.append(newPrompt)
    print('\n프롬프트가 추가되었습니다!')


# 2. 프롬프트 목록
def print_prompt():
    print('=== 프롬프트 목록 ===')

    for i, prompt in enumerate(prompts, start=1):
        print(f"{i}. [{category_map[prompt.category]}] {prompt.title} {' ⭐' if prompt.favorite else ''}")

    if len(prompts) == 0:
        print('\n등록된 프롬프트가 없습니다.')
    else:
        print(f'\n총 {len(prompts)}개의 프롬프트가 있습니다.')
    

# 3. 프롬프트 카테고리별 조회
def print_category():
    print("""
=== 카테고리별 조회 ===
1) 텍스트 생성
2) 이미지 생성
3) 영상 생성
4) 페르소나
5) 자동화
6) 기타
선택: """, end='')
    select = input()

    if not select.isdigit() or int(select) < 1 or int(select) > 6:
        print("########################################")
        print("1~6 사이의 숫자를 입력해주세요.")
        print("########################################")
        return
    
    category = int(select)

    print(f"\n[{category_map[category]}] 카테고리 프롬프트:")

    filtered_prompts = [p for p in prompts if p.category == category]

    for i, prompt in enumerate(filtered_prompts, start=1):
        print(f"{i}. {prompt.title} {' ⭐' if prompt.favorite else ''}")

    if len(filtered_prompts) == 0:
        print("등록된 프롬프트가 없습니다.")
    else:
        print(f"\n총 {len(filtered_prompts)}개의 프롬프트가 있습니다.")


# 4. 프롬프트 검색
def search_prompt():
    print('\n=== 프롬프트 검색 ===')
    print('검색어: ', end='')

    keyword = input()

    filtered_prompts = [p for p in prompts if keyword in p.title or keyword in p.content]

    for i, prompt in enumerate(filtered_prompts, start=1):
        print(f"{i}. [{category_map[prompt.category]}] {prompt.title} {' ⭐' if prompt.favorite else ''}")

    if len(filtered_prompts) == 0:
        print('해당 검색어를 포함하는 프롬프트가 없습니다.')
    else:
        print(f'\n총 {len(filtered_prompts)}개의 프롬프트를 찾았습니다.')


# 5. 프롬프트 상세 보기
def detail_prompt():
    print('\n=== 프롬프트 상세 보기 ===')
    print('번호 입력: ', end='')

    select = input()

    if not select.isdigit() or int(select) < 1 or int(select) > len(prompts):
        print("########################################")
        print("1~", len(prompts), " 사이의 숫자를 입력해주세요.")
        print("########################################")
        return

    prompt = prompts[int(select) - 1]
    print('-------------------------------------------')
    print(f"\n제목: {prompt.title}")
    print(f"카테고리: {category_map[prompt.category]}")
    print(f"즐겨찾기: {'⭐' if prompt.favorite else ''}")
    print('-------------------------------------------')
    print(f"내용: {prompt.content}")
    print('-------------------------------------------')


# 6. 프롬프트 즐겨찾기 관리
def print_bookmark():
    print('\n=== 프롬프트 즐겨찾기 관리 ===')
    print('프롬프트 번호 입력: ', end='')

    select = input()

    if not select.isdigit() or int(select) < 1 or int(select) > len(prompts):
        print("########################################")
        print("1~", len(prompts), " 사이의 숫자를 입력해주세요.")
        print("########################################")
        return

    prompt = prompts[int(select) - 1]
    prompt.favorite = not prompt.favorite
    
    print(f"'{prompt.title}' 프롬프트를 {'추가했습니다' if prompt.favorite else '삭제했습니다'}!")


# 7. 프롬프트 즐겨찾기 목록
def print_bookmark_list():
    print('\n=== 즐겨찾기 목록 ===')

    filtered_prompts = [p for p in prompts if p.favorite]

    for i, prompt in enumerate(filtered_prompts, start=1):
        print(f"{i}. [{category_map[prompt.category]}] {prompt.title} {' ⭐' if prompt.favorite else ''}")

    if len(filtered_prompts) == 0:
        print('\n등록된 프롬프트가 없습니다.')
    else:
        print(f'\n총 {len(filtered_prompts)}개의 프롬프트가 있습니다.')


# 프로그램 main 함수
def main():
    while True:
        select_number = main_menu()

        match select_number:
            case -1:
                continue
            case 0:
                print("\n프로그램을 종료합니다")
                break
            case 1:
                add_prompt()
            case 2:
                print_prompt()
            case 3:
                print_category()
            case 4:
                search_prompt()
            case 5:
                detail_prompt()
            case 6:
                print_bookmark()
            case 7:
                print_bookmark_list()
            case _:
                print("\n미확인 숫자 입력 오류")

        print('\n계속하려면 아무 키나 입력하세요.')
        input()


# 프로그램 시작 진입점
if __name__ == "__main__":
    main()