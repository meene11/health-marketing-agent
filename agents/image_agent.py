"""
Pillow 기반 마케팅 이미지 자동 생성 에이전트.
1080x1080 정사각형. 완전 무료.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CATEGORY_THEMES = {
    "건강/다이어트": {
        "bg":      "#0F3D2E",
        "accent":  "#2ECC71",
        "light":   "#A8F0C6",
        "dark":    "#071F17",
    },
    "뷰티": {
        "bg":      "#2D0A1F",
        "accent":  "#E91E8C",
        "light":   "#F9A8D4",
        "dark":    "#160510",
    },
    "식품": {
        "bg":      "#2D1500",
        "accent":  "#FF6B35",
        "light":   "#FFD0B5",
        "dark":    "#160A00",
    },
    "운동": {
        "bg":      "#0A1628",
        "accent":  "#3B82F6",
        "light":   "#BFDBFE",
        "dark":    "#050B14",
    },
    "기타": {
        "bg":      "#1A0A2E",
        "accent":  "#8B5CF6",
        "light":   "#DDD6FE",
        "dark":    "#0D0517",
    },
}

OUTPUT_DIR = Path("generated_images")


def _hex(color: str) -> tuple:
    """HEX → RGB 튜플 변환."""
    c = color.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "malgun.ttf",
        "malgunbd.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _draw_gradient_bg(img: Image.Image, top_color: str, bottom_color: str):
    """세로 그라데이션 배경."""
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = _hex(top_color)
    r2, g2, b2 = _hex(bottom_color)
    h = img.height
    for y in range(h):
        t = y / h
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (img.width, y)], fill=(r, g, b))


def _draw_circle(draw, cx, cy, r, color, alpha=255):
    r_val, g_val, b_val = _hex(color)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(r_val, g_val, b_val, alpha))


def _draw_text_centered(draw, text: str, y: int, width: int, font_size: int, color: str, font=None):
    f = font or _load_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=f, fill=color)


def run_image_agent(product_name: str, category: str, intro: str) -> str:
    OUTPUT_DIR.mkdir(exist_ok=True)
    theme = CATEGORY_THEMES.get(category, CATEGORY_THEMES["기타"])

    W, H = 1080, 1080
    img = Image.new("RGBA", (W, H), "#000000")

    # ── 1. 그라데이션 배경 ──
    _draw_gradient_bg(img, theme["bg"], theme["dark"])

    draw = ImageDraw.Draw(img, "RGBA")

    # ── 2. 장식 원 (우측 상단) ──
    r1, g1, b1 = _hex(theme["accent"])
    draw.ellipse([700, -150, 1230, 380], fill=(r1, g1, b1, 30))
    draw.ellipse([780, -80, 1150, 290], fill=(r1, g1, b1, 20))

    # ── 3. 장식 원 (좌측 하단) ──
    draw.ellipse([-150, 750, 350, 1250], fill=(r1, g1, b1, 25))

    # ── 4. 중앙 카드 (반투명 흰색 박스) ──
    card_x1, card_y1, card_x2, card_y2 = 60, 300, 1020, 750
    draw.rounded_rectangle(
        [card_x1, card_y1, card_x2, card_y2],
        radius=30,
        fill=(255, 255, 255, 18),
        outline=(255, 255, 255, 40),
        width=1,
    )

    # ── 5. 상단 액센트 라인 ──
    draw.rounded_rectangle([60, 300, 1020, 310], radius=5, fill=theme["accent"])

    # ── 6. 카테고리 뱃지 ──
    badge_font = _load_font(28)
    bbox = draw.textbbox((0, 0), category, font=badge_font)
    bw = bbox[2] - bbox[0] + 40
    bx = (W - bw) // 2
    draw.rounded_rectangle([bx, 170, bx + bw, 230], radius=20, fill=theme["accent"])
    _draw_text_centered(draw, category, y=178, width=W, font_size=28, color="#FFFFFF", font=badge_font)

    # ── 7. 제품명 (큰 텍스트) ──
    name_short = product_name if len(product_name) <= 14 else product_name[:13] + "…"
    name_font = _load_font(80)
    _draw_text_centered(draw, name_short, y=355, width=W, font_size=80, color="#FFFFFF", font=name_font)

    # ── 8. 구분선 ──
    acc_r, acc_g, acc_b = _hex(theme["accent"])
    draw.line([(300, 480), (780, 480)], fill=(acc_r, acc_g, acc_b, 200), width=2)

    # ── 9. 한 줄 소개 ──
    intro_text = intro[:24] + "…" if len(intro) > 24 else intro
    intro_font = _load_font(36)
    _draw_text_centered(draw, intro_text, y=510, width=W, font_size=36, color=theme["light"], font=intro_font)

    # ── 10. 하단 포인트 3개 ──
    dots_y = 620
    for i, (dx, label) in enumerate([(-300, "PREMIUM"), (0, "NATURAL"), (300, "TRUSTED")]):
        cx = W // 2 + dx
        draw.ellipse([cx - 18, dots_y - 18, cx + 18, dots_y + 18], fill=theme["accent"])
        dot_font = _load_font(20)
        _draw_text_centered(draw, label, y=dots_y + 26, width=W, font_size=20, color=theme["light"], font=dot_font)

    # ── 11. 하단 바 (브랜딩) ──
    draw.rectangle([0, 940, W, H], fill=(0, 0, 0, 120))
    bottom_font = _load_font(26)
    _draw_text_centered(draw, "건강한 선택, 더 나은 내일", y=960, width=W, font_size=26,
                        color=theme["light"], font=bottom_font)
    sub_font = _load_font(20)
    _draw_text_centered(draw, "health-marketing-agent", y=1005, width=W, font_size=20,
                        color="#FFFFFF60", font=sub_font)

    # ── 저장 ──
    OUTPUT_DIR.mkdir(exist_ok=True)
    safe_name = product_name.replace(" ", "_")
    file_path = OUTPUT_DIR / f"{safe_name}.png"
    img.convert("RGB").save(str(file_path))

    print(f"  [Image] 이미지 생성 완료: {file_path}")
    return str(file_path)
