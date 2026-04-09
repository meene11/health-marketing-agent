from config.settings import settings


def run_publisher(
    title: str,
    content: str,
    image_path: str,
    strengths: str,
    intro: str,
    tone: str,
    platforms: list[str],
) -> dict:
    """선택된 플랫폼에 콘텐츠를 발행한다."""
    results = {}

    if "네이버 블로그" in platforms:
        print("  [Publisher] 네이버 블로그 발행 중...")
        from tools.naver_tools import post_to_naver_blog
        results["naver"] = post_to_naver_blog(title=title, content=content)

    if "WordPress" in platforms:
        print("  [Publisher] WordPress 발행 중...")
        from tools.wordpress_tools import post_to_wordpress
        results["wordpress"] = post_to_wordpress(title=title, content=content)

    if "인스타그램" in platforms:
        print("  [Publisher] 인스타그램 발행 중...")
        from tools.instagram_tools import post_to_instagram, build_caption
        caption = build_caption(title=title, intro=intro, strengths=strengths, tone=tone)
        results["instagram"] = post_to_instagram(image_path=image_path, caption=caption)

    return results
