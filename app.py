import streamlit as st

st.set_page_config(
    page_title="마케팅 자동 포스팅",
    page_icon="🌿",
    layout="centered",
)

st.title("🌿 건강 마케팅 자동 포스팅")
st.caption("제품 정보를 입력하면 AI가 마케팅 글을 작성하고 블로그에 자동 발행합니다.")
st.divider()

# ── 섹션 1: 제품 정보 ──────────────────────────────────────
st.subheader("📦 제품 정보")

col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("제품/서비스명 *", placeholder="예: 그린 다이어트 보조제")
with col2:
    category = st.selectbox(
        "카테고리 *",
        ["건강/다이어트", "뷰티", "식품", "운동", "기타"],
    )

intro = st.text_input("한 줄 소개 *", placeholder="예: 천연 성분으로 만든 체지방 감소 보조제")

st.divider()

# ── 섹션 2: 홍보 내용 ──────────────────────────────────────
st.subheader("✍️ 홍보 내용")

strengths = st.text_area(
    "핵심 강점 * (줄바꿈 또는 쉼표로 구분)",
    placeholder="예:\n천연 성분 100%\nFDA 안전성 인증\n3개월 효과 보장",
    height=100,
)

target = st.text_input("타겟 고객 *", placeholder="예: 30~40대 직장인 여성")

tone = st.radio(
    "글 톤앤매너 *",
    ["친근한", "전문적", "감성적"],
    horizontal=True,
)

st.divider()

# ── 섹션 3: 발행 설정 ──────────────────────────────────────
st.subheader("📢 발행 플랫폼")

platforms = st.multiselect(
    "발행할 플랫폼을 선택하세요 *",
    ["네이버 블로그", "WordPress", "Facebook"],
    default=["네이버 블로그", "WordPress"],
)

st.divider()

# ── 발행 버튼 ───────────────────────────────────────────────
ready = product_name and intro and strengths and target and platforms

if not ready:
    st.info("필수 항목(*)을 모두 입력하면 발행 버튼이 활성화됩니다.")

if st.button("🚀 자동 포스팅 시작", disabled=not ready, type="primary", use_container_width=True):
    with st.spinner("파이프라인 실행 중..."):
        from orchestrator.workflow import run_pipeline

        user_input = {
            "product_name": product_name,
            "category": category,
            "intro": intro,
            "strengths": strengths,
            "target": target,
            "tone": tone,
            "platforms": platforms,
        }

        try:
            final_state = run_pipeline(user_input)

            st.success("발행 완료!")
            st.markdown(f"**제목:** {final_state['title']}")

            # 생성된 이미지 미리보기
            if final_state.get("image_path"):
                st.image(final_state["image_path"], caption="생성된 홍보 이미지", width=400)

            # 발행 결과
            st.subheader("발행 결과")
            for platform, url in final_state["published_urls"].items():
                icon = {"naver": "N", "wordpress": "W", "facebook": "F"}.get(platform, "-")
                st.markdown(f"**[{icon}]** {url}")

            # 생성된 글 미리보기
            with st.expander("생성된 글 보기"):
                st.markdown(final_state["content"])

        except Exception as e:
            st.error(f"오류 발생: {e}")
