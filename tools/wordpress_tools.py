import httpx
import base64
from pathlib import Path
from config.settings import settings


def _get_auth_token() -> str:
    credentials = f"{settings.wordpress_username}:{settings.wordpress_app_password}"
    return base64.b64encode(credentials.encode()).decode()


def _upload_image(site: str, image_path: str, token: str) -> int | None:
    """이미지를 WordPress 미디어 라이브러리에 업로드하고 media ID를 반환한다."""
    path = Path(image_path)
    if not path.exists():
        return None

    url = f"https://public-api.wordpress.com/wp/v2/sites/{site}/media"
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Disposition": f'attachment; filename="{path.name}"',
        "Content-Type": "image/png",
    }
    try:
        response = httpx.post(url, content=path.read_bytes(), headers=headers, timeout=30)
        if response.status_code in (200, 201):
            return response.json().get("id")
    except Exception:
        pass
    return None


def post_to_wordpress(title: str, content: str, image_path: str = "") -> str:
    """WordPress.com REST API로 글을 발행한다."""
    if not settings.wordpress_site or not settings.wordpress_username or not settings.wordpress_app_password:
        return "WordPress 설정 미완료 (WORDPRESS_SITE, USERNAME, APP_PASSWORD 필요)"

    site = settings.wordpress_site.replace("https://", "").replace("http://", "").rstrip("/")
    token = _get_auth_token()

    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }

    # 이미지 업로드
    media_id = None
    if image_path:
        print("  [WordPress] 이미지 업로드 중...")
        media_id = _upload_image(site, image_path, token)
        if media_id:
            print(f"  [WordPress] 이미지 업로드 완료 (ID: {media_id})")

    payload = {
        "title": title,
        "content": content.replace("\n", "<br>"),
        "status": "publish",
    }
    if media_id:
        payload["featured_media"] = media_id

    url = f"https://public-api.wordpress.com/wp/v2/sites/{site}/posts"
    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code in (200, 201):
            data = response.json()
            return f"WordPress 발행 완료: {data.get('link', site)}"
        return f"WordPress 발행 실패 (status: {response.status_code}): {response.text[:200]}"
    except Exception as e:
        return f"WordPress 발행 오류: {e}"
