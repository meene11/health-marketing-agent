"""
instagrapi 기반 인스타그램 자동 업로드 (데모용).
개인 계정 사용 - 계정 정지 위험 있음, 포트폴리오 데모 목적으로만 사용.
"""

from config.settings import settings


def post_to_instagram(image_path: str, caption: str) -> str:
    """인스타그램에 이미지 + 캡션을 업로드한다."""
    if not settings.instagram_username or not settings.instagram_password:
        return "Instagram 설정 미완료 (INSTAGRAM_USERNAME, PASSWORD 필요)"

    try:
        from instagrapi import Client

        cl = Client()
        cl.login(settings.instagram_username, settings.instagram_password)
        print("  [Instagram] 로그인 완료.")

        media = cl.photo_upload(
            path=image_path,
            caption=caption,
        )
        url = f"https://www.instagram.com/p/{media.code}/"
        print(f"  [Instagram] 업로드 완료: {url}")
        return f"Instagram 발행 완료: {url}"

    except Exception as e:
        return f"Instagram 발행 실패: {e}"


def build_caption(title: str, intro: str, strengths: str, tone: str) -> str:
    """인스타그램용 캡션을 생성한다."""
    strengths_list = [s.strip() for s in strengths.replace(",", "\n").splitlines() if s.strip()]
    strengths_tags = " ".join(f"#{s.replace(' ', '')}" for s in strengths_list[:3])

    return f"""{title}

{intro}

{'✅ ' + strengths_list[0] if strengths_list else ''}
{'✅ ' + strengths_list[1] if len(strengths_list) > 1 else ''}
{'✅ ' + strengths_list[2] if len(strengths_list) > 2 else ''}

{strengths_tags} #건강 #다이어트 #헬스 #건강관리 #웰니스
""".strip()
