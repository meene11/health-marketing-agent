import httpx
from config.settings import settings


def run_notification(title: str, published_urls: dict) -> str:
    """발행 완료 시 슬랙으로 알림을 보낸다."""
    if not settings.slack_webhook_url:
        print("  [Notification] SLACK_WEBHOOK_URL 미설정, 건너뜀.")
        return "알림 건너뜀 (Slack 미설정)"

    lines = [f"*발행 완료!*", f"제목: {title}", ""]
    for platform, url in published_urls.items():
        emoji = {"naver": "N", "wordpress": "W", "instagram": "I"}.get(platform, "-")
        lines.append(f"[{emoji}] {url}")

    message = "\n".join(lines)

    try:
        response = httpx.post(
            settings.slack_webhook_url,
            json={"text": message},
            timeout=10,
        )
        if response.status_code == 200:
            print("  [Notification] 슬랙 알림 전송 완료!")
            return "슬랙 알림 완료"
        return f"슬랙 알림 실패 (status: {response.status_code})"
    except Exception as e:
        return f"슬랙 알림 오류: {e}"
