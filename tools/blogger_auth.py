"""
Blogger OAuth 2.0 최초 인증 스크립트.
최초 1회만 실행하면 blogger_token.json이 생성되어 이후 자동 갱신됩니다.

실행: python tools/blogger_auth.py
"""

import json
import httpx
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

TOKEN_FILE = Path("blogger_token.json")
AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
SCOPES = "https://www.googleapis.com/auth/blogger"


def run_auth():
    from config.settings import settings

    if not settings.blogger_client_id or not settings.blogger_client_secret:
        print("❌ .env에 BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET을 먼저 입력하세요.")
        return

    # 인증 URL 생성
    params = {
        "client_id": settings.blogger_client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{AUTH_ENDPOINT}?{urlencode(params)}"

    print("\n=== Blogger OAuth 인증 ===")
    print("아래 URL을 브라우저에서 열어 구글 계정으로 로그인하세요:")
    print(f"\n{auth_url}\n")
    webbrowser.open(auth_url)

    code = input("브라우저에서 받은 인증 코드를 여기에 붙여넣으세요: ").strip()

    # 토큰 발급
    response = httpx.post(TOKEN_ENDPOINT, data={
        "client_id": settings.blogger_client_id,
        "client_secret": settings.blogger_client_secret,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }, timeout=10)

    if response.status_code != 200:
        print(f"❌ 토큰 발급 실패: {response.text}")
        return

    token_data = response.json()
    TOKEN_FILE.write_text(json.dumps(token_data, indent=2))
    print(f"\n✅ 인증 완료! blogger_token.json 저장됨.")
    print(f"   이제 python app.py로 실행하면 됩니다.")


if __name__ == "__main__":
    run_auth()
