"""
Pillow 기반 마케팅 이미지 자동 생성 에이전트.
인스타그램 정사각형 (1080x1080) 기준. 완전 무료.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


CATEGORY_COLORS = {
    "건강/다이어트": ("#2ECC71", "#FFFFFF"),
    "뷰티":          ("#E91E8C", "#FFFFFF"),
    "식품":          ("#FF6B35", "#FFFFFF"),
    "운동":          ("#3498DB", "#FFFFFF"),
    "기타":          ("#8E44AD", "#FFFFFF"),
}

OUTPUT_DIR = Path("generated_images")


def run_image_agent(product_name: str, category: str, intro: str) -> str:
    """
    제품 홍보 이미지를 생성하고 파일 경로를 반환한다.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    bg_color, text_color = CATEGORY_COLORS.get(category, ("#2C3E50", "#FFFFFF"))

    img = Image.new("RGB", (1080, 1080), color=bg_color)
    draw = ImageDraw.Draw(img)

    # 배경에 반투명 오버레이 효과 (어두운 하단 띠)
    overlay = Image.new("RGBA", (1080, 300), (0, 0, 0, 120))
    img.paste(Image.new("RGB", (1080, 300), "#000000"), (0, 780))

    draw = ImageDraw.Draw(img)

    # 카테고리 뱃지
    draw.rounded_rectangle([40, 40, 240, 90], radius=20, fill="#FFFFFF40")
    _draw_text_centered(draw, category, y=55, width=1080, font_size=24, color="#FFFFFF")

    # 제품명 (중앙 큰 텍스트)
    _draw_text_centered(draw, product_name, y=420, width=1080, font_size=72, color=text_color)

    # 구분선
    draw.line([(340, 530), (740, 530)], fill="#FFFFFF", width=2)

    # 한 줄 소개
    intro_short = intro[:30] + "..." if len(intro) > 30 else intro
    _draw_text_centered(draw, intro_short, y=560, width=1080, font_size=32, color="#FFFFFFCC")

    # 하단 브랜딩
    _draw_text_centered(draw, "건강한 선택", y=820, width=1080, font_size=28, color="#FFFFFF")
    _draw_text_centered(draw, "auto-marketing-agent", y=870, width=1080, font_size=20, color="#FFFFFF80")

    # 저장
    safe_name = product_name.replace(" ", "_")
    file_path = OUTPUT_DIR / f"{safe_name}.png"
    img.save(str(file_path))

    print(f"  [Image] 이미지 생성 완료: {file_path}")
    return str(file_path)


def _draw_text_centered(draw, text: str, y: int, width: int, font_size: int, color: str):
    """텍스트를 수평 중앙에 그린다."""
    try:
        font = ImageFont.truetype("malgun.ttf", font_size)  # Windows 맑은 고딕
    except Exception:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=font, fill=color)
