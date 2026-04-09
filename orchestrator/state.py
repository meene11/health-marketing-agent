from typing import TypedDict


class MarketingState(TypedDict):
    # 사용자 입력
    product_name: str        # 제품/서비스명
    category: str            # 카테고리
    intro: str               # 한 줄 소개
    strengths: str           # 핵심 강점
    target: str              # 타겟 고객
    tone: str                # 톤앤매너 (친근한/전문적/감성적)
    platforms: list[str]     # 발행 플랫폼 선택

    # 에이전트 결과
    research_result: str     # Research Agent 수집 자료
    title: str               # 생성된 제목
    content: str             # 생성된 본문
    image_path: str          # 생성된 이미지 경로

    # 발행 결과
    published_urls: dict     # { naver, wordpress, instagram }
