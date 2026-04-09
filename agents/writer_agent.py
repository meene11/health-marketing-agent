"""
마케팅 블로그 포스팅 생성 에이전트.
톤앤매너에 따라 다른 템플릿 사용. LLM 없음 -> 비용 $0.
"""

TONE_OPENERS = {
    "친근한": {
        "hook": "혹시 이런 고민 해보신 적 있으신가요?",
        "cta": "지금 바로 시작해보세요! 작은 변화가 큰 차이를 만듭니다 :)",
    },
    "전문적": {
        "hook": "최신 연구 결과에 따르면, 다음과 같은 사실이 밝혀졌습니다.",
        "cta": "전문가 권장 솔루션으로 건강한 변화를 경험하시기 바랍니다.",
    },
    "감성적": {
        "hook": "건강한 나를 만나는 여정, 지금 시작해도 늦지 않았습니다.",
        "cta": "더 나은 내일을 위한 첫 걸음, 함께 내딛어 보시겠어요?",
    },
}


def run_writer(
    product_name: str,
    category: str,
    intro: str,
    strengths: str,
    target: str,
    tone: str,
    research_result: str,
) -> dict:
    """마케팅 블로그 포스팅 생성. 반환: { title, content }"""

    tone_data = TONE_OPENERS.get(tone, TONE_OPENERS["친근한"])
    strengths_list = [s.strip() for s in strengths.replace(",", "\n").splitlines() if s.strip()]

    title = _generate_title(product_name, category, tone)
    content = _generate_content(
        product_name=product_name,
        category=category,
        intro=intro,
        strengths_list=strengths_list,
        target=target,
        tone_data=tone_data,
        research_result=research_result,
    )

    print(f"  [Writer] 포스팅 생성 완료: {title}")
    return {"title": title, "content": content}


def _generate_title(product_name: str, category: str, tone: str) -> str:
    patterns = {
        "친근한": [
            f"{product_name}, 써보니까 진짜 달랐어요",
            f"{category} 고민이라면? {product_name} 추천드려요",
            f"솔직 후기: {product_name} 한 달 사용기",
        ],
        "전문적": [
            f"{product_name} 성분 분석 및 효과 검토",
            f"전문가가 추천하는 {category} 솔루션: {product_name}",
            f"{product_name}의 과학적 근거와 기대 효과",
        ],
        "감성적": [
            f"나를 위한 선택, {product_name}과 함께한 변화",
            f"{product_name}이 내 {category} 습관을 바꿨습니다",
            f"더 건강한 내가 되고 싶다면: {product_name} 이야기",
        ],
    }
    import hashlib
    idx = int(hashlib.md5(product_name.encode()).hexdigest(), 16) % 3
    return patterns.get(tone, patterns["친근한"])[idx]


def _generate_content(
    product_name, category, intro, strengths_list, target, tone_data, research_result
) -> str:
    strengths_md = "\n".join(f"- **{s}**" for s in strengths_list) if strengths_list else "- 다양한 장점 보유"

    # 연구 자료에서 핵심 문장 추출 (첫 3줄)
    research_lines = [
        line.strip() for line in research_result.splitlines()
        if line.strip().startswith("-")
    ][:3]
    research_md = "\n".join(research_lines) if research_lines else "- 관련 건강 연구 자료 참고"

    return f"""## {tone_data['hook']}

{target}를 위한 {category} 솔루션, **{product_name}**을 소개합니다.

> {intro}

---

## {product_name}의 핵심 강점

{strengths_md}

---

## 관련 건강 정보

전문가 자료와 최신 연구를 바탕으로 {product_name}의 효과를 확인해보세요.

{research_md}

---

## 이런 분께 추천드려요

- {target}
- {category}에 관심 있으신 분
- 건강한 생활 습관을 만들고 싶으신 분

---

{tone_data['cta']}

*본 포스팅은 자동화 마케팅 시스템으로 작성되었습니다.*
""".strip()
