"""
Supabase 건강 DB 조회 도구.

테이블 구조:
- documents_v2: 건강식품, 건강식품_논문, 다이어트_논문 (200 토큰 청크, 메인)
- parent_chunks: 건강기사, 건강식품_논문, 네이버블로그 (1600 토큰, 보조)

사용 컬럼: category, content, source_file (embedding 제외)
"""

import httpx
from config.settings import settings

# 사용자 카테고리 → DB 카테고리 매핑
CATEGORY_MAP = {
    "건강/다이어트": ["다이어트_논문", "건강식품", "건강식품_논문"],
    "뷰티":          ["건강식품", "건강식품_논문"],
    "식품":          ["건강식품", "건강식품_논문", "다이어트_논문"],
    "운동":          ["다이어트_논문", "건강식품_논문"],
    "기타":          ["건강식품", "기타"],
}


def fetch_health_data(keyword: str, category: str, limit: int = 5) -> str:
    """
    Supabase에서 카테고리 관련 건강 데이터를 조회한다.
    documents_v2 (논문/연구 자료) + parent_chunks (기사) 를 함께 조회.
    """
    if not settings.supabase_url or not settings.supabase_key:
        return "Supabase 미설정 - 건강 DB 조회 건너뜀"

    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
    }

    db_categories = CATEGORY_MAP.get(category, ["건강식품", "건강식품_논문"])
    results = []

    # 1. documents_v2 에서 논문/연구 자료 조회
    for cat in db_categories[:2]:
        r = httpx.get(
            f"{settings.supabase_url}/rest/v1/documents_v2",
            headers=headers,
            params={
                "select": "category,content,source_file",
                "category": f"eq.{cat}",
                "limit": str(limit // 2 + 1),
                "order": "created_at.desc",
            },
            timeout=10,
        )
        if r.status_code == 200:
            results.extend(r.json())

    # 2. parent_chunks 에서 건강 기사 조회 (더 긴 문맥)
    r = httpx.get(
        f"{settings.supabase_url}/rest/v1/parent_chunks",
        headers=headers,
        params={
            "select": "category,content,source_file",
            "category": "eq.건강식품_논문",
            "limit": "2",
            "order": "created_at.desc",
        },
        timeout=10,
    )
    if r.status_code == 200:
        results.extend(r.json())

    if not results:
        return "관련 건강 데이터 없음"

    lines = []
    for item in results[:limit]:
        content = item.get("content", "")[:300]
        source = item.get("source_file", "").split("/")[-1]
        cat = item.get("category", "")
        lines.append(f"[{cat}] {content}\n(출처: {source})")

    print(f"  [Supabase] 건강 데이터 {len(lines)}건 조회 완료")
    return "\n\n".join(lines)
