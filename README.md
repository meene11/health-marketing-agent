# 🌿 Health Marketing Agent

> AI 멀티에이전트 기반 건강 마케팅 자동 포스팅 시스템  
> **실행 비용 $0** · Streamlit 웹 UI · WordPress + Blogger 동시 발행

**🚀 배포 URL**: [Streamlit 앱 URL을 여기에 입력하세요]

---

## 프로젝트 소개

사용자가 **웹 UI**에 제품/서비스 정보를 입력하면, 멀티에이전트 파이프라인이 건강 마케팅 콘텐츠를 자동 생성하고 **WordPress · Google Blogger**에 동시 발행하는 마케팅 자동화 시스템입니다.

발행 완료 시 **Slack**으로 알림을 받을 수 있습니다.

---

## 시스템 아키텍처

```
[Streamlit 웹 UI]
  사용자 입력: 제품명, 카테고리, 핵심 강점, 타겟 고객, 톤앤매너, 발행 플랫폼
        ↓
[Orchestrator - LangGraph StateGraph]
        ↓
[Research Agent]   Supabase 건강 DB + DuckDuckGo 웹 검색
[Writer Agent]     마케팅 블로그 글 자동 생성 (LLM 없음, $0)
[Image Agent]      Pillow 기반 1080x1080 홍보 이미지 자동 생성
[Publisher Agent]  WordPress REST API + Blogger API v3 동시 발행
[Notify Agent]     Slack Webhook 발행 완료 알림
```

---

## 에이전트 구성

| 에이전트 | 역할 | 기술 |
|---|---|---|
| Research Agent | 건강 DB 조회 + 웹 검색으로 자료 수집 | Supabase + DuckDuckGo |
| Writer Agent | 마케팅 블로그 포스팅 자동 생성 | Python 템플릿 (LLM 없음) |
| Image Agent | 카테고리별 홍보 이미지 생성 | Pillow |
| Publisher Agent | WordPress + Blogger 동시 발행 | REST API + OAuth2 |
| Notification Agent | 발행 완료 Slack 알림 | Slack Incoming Webhook |

---

## 기술 스택

| 분류 | 기술 |
|---|---|
| 웹 UI | Streamlit |
| 파이프라인 오케스트레이터 | LangGraph (StateGraph) |
| 에이전트 프레임워크 | LangChain |
| 데이터베이스 | Supabase (PostgreSQL) |
| 이미지 생성 | Pillow |
| 발행 플랫폼 | WordPress.com REST API, Google Blogger API v3 |
| 인증 | OAuth2 (Google, WordPress.com) |
| 알림 | Slack Incoming Webhook |
| 배포 | Streamlit Community Cloud |

---

## 실행 비용

| 항목 | 비용 |
|---|---|
| Streamlit Cloud 호스팅 | 무료 |
| LangGraph / LangChain | 무료 |
| Supabase | 무료 |
| Pillow 이미지 생성 | 무료 |
| WordPress.com | 무료 |
| Google Blogger | 무료 |
| DuckDuckGo 검색 | 무료 |
| Slack 알림 | 무료 |
| **합계** | **$0 / 월** |

---

## 웹 UI 입력 항목

```
📦 제품 정보
  - 제품/서비스명
  - 카테고리 (건강/다이어트, 뷰티, 식품, 운동, 기타)
  - 한 줄 소개

✍️ 홍보 내용
  - 핵심 강점 (줄바꿈 또는 쉼표 구분)
  - 타겟 고객
  - 톤앤매너 (친근한 / 전문적 / 감성적)

📢 발행 플랫폼
  - WordPress, Blogger (기본 선택)
  - Facebook (추후 지원 예정)
```

---

## 설치 및 실행 (로컬)

```bash
git clone https://github.com/meene11/health-marketing-agent.git
cd health-marketing-agent

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

# Blogger OAuth2 최초 인증 (1회만)
set PYTHONPATH=%CD%
python tools/blogger_auth.py

# WordPress OAuth2 최초 인증 (1회만)
python tools/wordpress_auth.py

streamlit run app.py
```

---

## Streamlit Cloud 배포

1. [share.streamlit.io](https://share.streamlit.io) 접속
2. **New app** → Repository: `meene11/health-marketing-agent`
3. Branch: `main` / Main file: `app.py`
4. **Settings → Secrets** 에 아래 형식으로 입력:

```toml
SUPABASE_URL = "..."
SUPABASE_KEY = "..."
WORDPRESS_SITE = "https://yoursite.wordpress.com"
WORDPRESS_ACCESS_TOKEN = "..."
BLOGGER_BLOG_ID = "..."
BLOGGER_CLIENT_ID = "..."
BLOGGER_CLIENT_SECRET = "..."
BLOGGER_REFRESH_TOKEN = "..."
SLACK_WEBHOOK_URL = "..."
```

---

## 관련 프로젝트

- [auto-multi-agent](https://github.com/meene11/auto-multi-agent) — IT 뉴스 자동 블로그 발행 시스템 (선행 프로젝트)
