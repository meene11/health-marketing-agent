"""
WordPress.com OAuth2 최초 인증 스크립트.
최초 1회만 실행하면 WORDPRESS_ACCESS_TOKEN을 발급받습니다.
WordPress.com access token은 만료되지 않습니다.

실행 전 준비:
1. https://developer.wordpress.com/apps/ 에서 앱 설정 열기
2. Redirect URI에 http://localhost:8888 추가 후 저장

실행: python tools/wordpress_auth.py
"""

import httpx
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs

REDIRECT_URI = "http://localhost:8888"
AUTH_URL = "https://public-api.wordpress.com/oauth2/authorize"
TOKEN_URL = "https://public-api.wordpress.com/oauth2/token"

code_holder = {"code": None}


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        code_holder["code"] = params.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write("✅ 인증 완료! 이 창을 닫으세요.".encode("utf-8"))

    def log_message(self, format, *args):
        pass  # 로그 출력 억제


def run_auth():
    from config.settings import settings

    client_id = settings.wordpress_client_id if hasattr(settings, 'wordpress_client_id') else ""
    client_secret = settings.wordpress_client_secret if hasattr(settings, 'wordpress_client_secret') else ""

    # 직접 env에서 읽기 (settings에 없을 수 있음)
    import os
    client_id = client_id or os.environ.get("WORDPRESS_CLIENT_ID", "")
    client_secret = client_secret or os.environ.get("WORDPRESS_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        print("❌ .env에 WORDPRESS_CLIENT_ID, WORDPRESS_CLIENT_SECRET을 먼저 입력하세요.")
        return

    params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "global",
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"

    # 로컬 서버 시작 (코드 수신용)
    server = HTTPServer(("localhost", 8888), OAuthHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    print("\n=== WordPress.com OAuth2 인증 ===")
    print("브라우저가 자동으로 열립니다. WordPress.com 계정으로 로그인하세요.")
    print(f"\n수동으로 열려면: {auth_url}\n")
    webbrowser.open(auth_url)

    thread.join(timeout=120)
    code = code_holder["code"]

    if not code:
        print("❌ 인증 코드를 받지 못했습니다. 다시 시도하세요.")
        return

    # access token 발급
    response = httpx.post(TOKEN_URL, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }, timeout=10)

    if response.status_code != 200:
        print(f"❌ 토큰 발급 실패: {response.text}")
        return

    token_data = response.json()
    access_token = token_data.get("access_token")

    print(f"\n✅ 인증 완료!")
    print(f"\n.env 파일과 Streamlit Secrets에 아래 값을 추가하세요:\n")
    print(f"WORDPRESS_ACCESS_TOKEN={access_token}\n")


if __name__ == "__main__":
    run_auth()
