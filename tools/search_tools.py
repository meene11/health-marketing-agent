from duckduckgo_search import DDGS


def search_health_info(keyword: str, max_results: int = 5) -> str:
    """DuckDuckGo로 건강 관련 정보를 검색한다."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                f"{keyword} 건강 효능 다이어트",
                region="kr-kr",
                max_results=max_results,
            ))
        if not results:
            return "검색 결과 없음"

        lines = []
        for r in results:
            lines.append(f"- {r.get('title', '')}: {r.get('body', '')[:150]}")
        return "\n".join(lines)
    except Exception as e:
        return f"검색 실패: {e}"
