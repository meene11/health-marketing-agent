import httpx
from config.settings import settings


def fetch_health_data(keyword: str, limit: int = 5) -> str:
    """Supabase 건강 DB에서 키워드 관련 데이터를 조회한다."""
    if not settings.supabase_url or not settings.supabase_key:
        return "Supabase 설정 없음 - 건강 DB 조회 건너뜀"

    url = f"{settings.supabase_url}/rest/v1/{settings.supabase_health_table}"
    headers = {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
    }
    params = {
        "limit": str(limit),
        "order": "created_at.desc",
    }

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not data:
                return "건강 DB에 데이터 없음"
            lines = []
            for item in data:
                # 테이블 구조에 맞게 유연하게 처리
                text = (
                    item.get("content") or
                    item.get("description") or
                    item.get("summary") or
                    str(item)[:200]
                )
                lines.append(f"- {text}")
            return "\n".join(lines)
        return f"DB 조회 실패 (status: {response.status_code})"
    except Exception as e:
        return f"DB 조회 오류: {e}"
