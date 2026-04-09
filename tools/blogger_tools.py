"""
Google Blogger API v3 기반 자동 포스팅.

필요한 설정:
1. Google Cloud Console에서 Blogger API v3 활성화
2. OAuth 2.0 클라이언트 ID 생성 (데스크톱 앱)
3. 최초 1회 인증 후 token.json 자동 저장 → 이후 자동 갱신

필요한 .env 값:
- BLOGGER_BLOG_ID: 블로그 ID (blogger.com 대시보드 URL에서 확인)
- BLOGGER_CLIENT_ID: OAuth 클라이언트 ID
- BLOGGER_CLIENT_SECRET: OAuth 클라이언트 시크릿
"""

import json
import httpx
from pathlib import Path
from config.settings import settings

TOKEN_FILE = Path("blogger_token.json")
BLOGGER_API = "https://www.googleapis.com/blogger/v3"
AUTH_URL = "https://oauth2.googleapis.com/token"


def _get_access_token() -> str:
    """저장된 토큰으로 액세스 토큰을 가져온다. 만료 시 자동 갱신.
    환경변수 BLOGGER_REFRESH_TOKEN 우선, 없으면 blogger_token.json 사용."""

    # 1. 환경변수 우선 (배포 환경)
    refresh_token = settings.blogger_refresh_token

    # 2. 로컬 파일 폴백
    if not refresh_token:
        if not TOKEN_FILE.exists():
            raise RuntimeError(
                "blogger_token.json이 없습니다. "
                "python tools/blogger_auth.py 를 먼저 실행해 인증을 완료하세요."
            )
        token_data = json.loads(TOKEN_FILE.read_text())
        refresh_token = token_data.get("refresh_token")

    if not refresh_token:
        raise RuntimeError("refresh_token이 없습니다. 재인증이 필요합니다.")

    # 액세스 토큰 갱신
    response = httpx.post(AUTH_URL, data={
        "client_id": settings.blogger_client_id,
        "client_secret": settings.blogger_client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"토큰 갱신 실패: {response.text}")

    new_data = response.json()
    # 갱신된 토큰 저장
    token_data["access_token"] = new_data["access_token"]
    TOKEN_FILE.write_text(json.dumps(token_data))

    return new_data["access_token"]


def _image_to_base64_tag(image_path: str) -> str:
    """이미지 파일을 base64 인코딩해서 HTML img 태그로 반환한다."""
    from pathlib import Path
    import base64
    path = Path(image_path)
    if not path.exists():
        return ""
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<img src="data:image/png;base64,{data}" style="width:100%;max-width:600px;display:block;margin:0 auto 20px;" />'


def post_to_blogger(title: str, content: str, image_path: str = "") -> str:
    """Blogger에 포스팅을 발행한다."""
    if not settings.blogger_blog_id:
        return "Blogger 설정 미완료 (BLOGGER_BLOG_ID 필요)"
    if not settings.blogger_client_id or not settings.blogger_client_secret:
        return "Blogger 설정 미완료 (BLOGGER_CLIENT_ID, SECRET 필요)"

    try:
        access_token = _get_access_token()
    except RuntimeError as e:
        return f"Blogger 인증 오류: {e}"

    url = f"{BLOGGER_API}/blogs/{settings.blogger_blog_id}/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # 이미지 삽입 (base64)
    image_tag = ""
    if image_path:
        print("  [Blogger] 이미지 변환 중...")
        image_tag = _image_to_base64_tag(image_path)

    # 마크다운 → HTML 기본 변환
    html_content = content.replace("\n", "<br>")
    if image_tag:
        html_content = image_tag + html_content

    payload = {
        "kind": "blogger#post",
        "title": title,
        "content": html_content,
    }

    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code in (200, 201):
            data = response.json()
            post_url = data.get("url", f"https://{settings.blogger_blog_id}.blogspot.com")
            print(f"  [Blogger] 발행 완료: {post_url}")
            return f"Blogger 발행 완료: {post_url}"
        return f"Blogger 발행 실패 (status: {response.status_code}): {response.text[:200]}"
    except Exception as e:
        return f"Blogger 발행 오류: {e}"
