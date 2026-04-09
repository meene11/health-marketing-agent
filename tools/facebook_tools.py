"""
Facebook Graph API 기반 페이지 자동 포스팅.
이미지 + 캡션 함께 발행. 공식 API, 완전 무료.

필요한 것:
- Facebook Page (개인 프로필 X)
- FACEBOOK_PAGE_ID
- FACEBOOK_PAGE_ACCESS_TOKEN (장기 토큰 권장)
"""

import httpx
from config.settings import settings


def post_to_facebook(image_path: str, caption: str) -> str:
    """Facebook 페이지에 이미지 + 캡션을 발행한다."""
    if not settings.facebook_page_id or not settings.facebook_page_access_token:
        return "Facebook 설정 미완료 (FACEBOOK_PAGE_ID, PAGE_ACCESS_TOKEN 필요)"

    url = f"https://graph.facebook.com/v19.0/{settings.facebook_page_id}/photos"

    try:
        with open(image_path, "rb") as img_file:
            response = httpx.post(
                url,
                data={
                    "message": caption,
                    "access_token": settings.facebook_page_access_token,
                },
                files={"source": ("image.png", img_file, "image/png")},
                timeout=30,
            )

        if response.status_code == 200:
            data = response.json()
            post_id = data.get("post_id") or data.get("id", "")
            page_url = f"https://www.facebook.com/{settings.facebook_page_id}"
            print(f"  [Facebook] 발행 완료!")
            return f"Facebook 발행 완료: {page_url}"

        return f"Facebook 발행 실패 (status: {response.status_code}): {response.text[:200]}"

    except FileNotFoundError:
        return "Facebook 발행 실패: 이미지 파일을 찾을 수 없습니다."
    except Exception as e:
        return f"Facebook 발행 오류: {e}"


def build_caption(title: str, intro: str, strengths: str, tone: str) -> str:
    """Facebook용 캡션을 생성한다."""
    strengths_list = [s.strip() for s in strengths.replace(",", "\n").splitlines() if s.strip()]
    strengths_text = "\n".join(f"✅ {s}" for s in strengths_list[:3])
    hashtags = "#건강 #다이어트 #헬스 #건강관리 #웰니스 #건강식품"

    return f"""{title}

{intro}

{strengths_text}

{hashtags}
""".strip()
