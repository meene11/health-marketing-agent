import httpx
import base64
from config.settings import settings


def post_to_wordpress(title: str, content: str) -> str:
    """WordPress.com REST API로 글을 발행한다."""
    if not settings.wordpress_site or not settings.wordpress_username or not settings.wordpress_app_password:
        return "WordPress 설정 미완료 (WORDPRESS_SITE, USERNAME, APP_PASSWORD 필요)"

    site = settings.wordpress_site.replace("https://", "").replace("http://", "").rstrip("/")
    url = f"https://public-api.wordpress.com/wp/v2/sites/{site}/posts"

    credentials = f"{settings.wordpress_username}:{settings.wordpress_app_password}"
    token = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "title": title,
        "content": content.replace("\n", "<br>"),
        "status": "publish",
    }

    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code in (200, 201):
            data = response.json()
            return f"WordPress 발행 완료: {data.get('link', site)}"
        return f"WordPress 발행 실패 (status: {response.status_code}): {response.text[:200]}"
    except Exception as e:
        return f"WordPress 발행 오류: {e}"
