from tools.search_tools import search_health_info
from tools.supabase_tools import fetch_health_data


def run_research(product_name: str, category: str, strengths: str) -> str:
    """
    건강 DB + DuckDuckGo 검색으로 마케팅 자료를 수집한다.
    """
    print("  [Research] Supabase 건강 DB 조회 중...")
    db_result = fetch_health_data(keyword=product_name)

    print("  [Research] DuckDuckGo 웹 검색 중...")
    search_result = search_health_info(keyword=f"{product_name} {category}")

    research = f"""
=== 건강 DB 데이터 ===
{db_result}

=== 웹 검색 결과 ===
{search_result}

=== 제품 핵심 강점 ===
{strengths}
""".strip()

    print("  [Research] 자료 수집 완료.")
    return research
