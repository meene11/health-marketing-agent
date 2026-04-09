# health-marketing-agent

> AI-powered multi-agent system that auto-generates and publishes health & wellness marketing content across Naver, WordPress, and Instagram using LangChain, LangGraph orchestrator, and Streamlit UI.

---

## 프로젝트 소개

사용자가 **웹 UI**에 제품/서비스 정보를 입력하면, 멀티에이전트 파이프라인이 건강 관련 마케팅 콘텐츠를 자동 생성하고 **네이버 블로그 · WordPress · 인스타그램**에 동시 발행하는 마케팅 자동화 시스템입니다.

발행 완료 시 **카카오톡 또는 슬랙**으로 알림을 받을 수 있습니다.

---

## 시스템 아키텍처

```
[Streamlit 웹 UI]
  사용자 입력: 제품명, 카테고리, 핵심 강점, 타겟 고객, 톤앤매너, 발행 플랫폼
        ↓
[Orchestrator - LangGraph StateGraph]
        ↓
[Research Agent]       Supabase 건강 DB + DuckDuckGo 웹 검색
[Writer Agent]         마케팅 블로그 글 자동 생성
[Image Agent]          Pillow 기반 홍보 이미지 자동 생성
        ↓
[Publisher Agent]
  ├─ 네이버 블로그   Selenium 브라우저 자동화
  ├─ WordPress      REST API 자동 발행
  └─ 인스타그램     instagrapi 자동 업로드 (데모)
        ↓
[Notification Agent]
  └─ 카카오톡 or 슬랙 "발행 완료" 알림
```

---

## 에이전트 구성

| 에이전트 | 역할 | 방식 |
|---|---|---|
| Research Agent | 건강 DB 조회 + 웹 검색으로 관련 자료 수집 | Supabase + DuckDuckGo |
| Writer Agent | 마케팅 블로그 포스팅 생성 | Python 템플릿 |
| Image Agent | 제품 홍보 이미지 자동 생성 | Pillow (무료) |
| Publisher Agent | 3개 플랫폼 동시 발행 | API + Selenium |
| Notification Agent | 발행 완료 알림 발송 | 카카오톡 / 슬랙 웹훅 |

---

## 기술 스택

| 분류 | 기술 |
|---|---|
| 웹 UI | Streamlit |
| 파이프라인 오케스트레이터 | LangGraph |
| LLM 프레임워크 | LangChain |
| 데이터베이스 | Supabase |
| 이미지 생성 | Pillow |
| 웹 자동화 | Selenium, pyautogui, pyperclip |
| 인스타그램 | instagrapi |
| 알림 | 카카오톡 API / 슬랙 웹훅 |

---

## 웹 UI 입력 필드

```
📦 제품 정보
  - 제품/서비스명
  - 카테고리 (건강/다이어트, 뷰티, 식품, 운동, 기타)
  - 한 줄 소개

✍️ 홍보 내용
  - 핵심 강점
  - 타겟 고객
  - 톤앤매너 (친근한 / 전문적 / 감성적)

📢 발행 설정
  - 플랫폼 선택 (네이버 / WordPress / 인스타그램)
```

---

## 실행 비용

| 항목 | 비용 |
|---|---|
| Streamlit UI | 무료 |
| LangGraph / LangChain | 무료 |
| Supabase | 무료 |
| Pillow 이미지 생성 | 무료 |
| WordPress.com API | 무료 |
| 네이버 Selenium | 무료 |
| 카카오톡 / 슬랙 알림 | 무료 |
| **합계** | **$0** |

---

## 설치 및 실행

```bash
git clone https://github.com/meene11/health-marketing-agent.git
cd health-marketing-agent

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# .env에 API 키 입력 후

streamlit run app.py
```

---

## 관련 프로젝트

- [auto-multi-agent](https://github.com/meene11/auto-multi-agent) — IT 뉴스 자동 블로그 발행 시스템 (선행 프로젝트)
