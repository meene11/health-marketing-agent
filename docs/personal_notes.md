# 📒 개인 기술 노트 — health-marketing-agent

> 나만 보는 문서. 계획, 개념 정리, 멘토 예상 질문 답변 모음.

---

## 1. 이 프로젝트를 왜 만드나?

### 배경
- 선행 프로젝트 `auto-multi-agent`에서 IT 뉴스 자동 발행을 구현함
- 멘토님이 원하는 학습 목표:
  - 멀티에이전트 설계
  - 오케스트레이터 (LangGraph)
  - LangChain 활용
  - 자동화 파이프라인
  - 발행 완료 알림 서비스
  - **고객이 웹 UI로 요청 → 자동 포스팅**

### 핵심 차이점 (선행 프로젝트 vs 이 프로젝트)

| | auto-multi-agent | health-marketing-agent |
|---|---|---|
| 입력 | 자동 (DB에서 가져옴) | 사용자가 웹에서 직접 입력 |
| 주제 | IT 뉴스 요약 | 건강/마케팅 홍보 글 |
| Research | DB 조회만 | DB + 웹 검색 (LangChain) |
| 이미지 | 없음 | Pillow 자동 생성 |
| 알림 | 없음 | 카카오톡/슬랙 |
| UI | 없음 | Streamlit 웹 UI |
| 플랫폼 | dev.to, Hashnode, 네이버 | 네이버, WordPress, 인스타 |

---

## 2. 전체 아키텍처 개념

### 왜 LangGraph인가?
- 멀티에이전트가 순서대로, 또는 조건에 따라 실행되어야 함
- LangGraph = 에이전트들을 **그래프 노드**로 연결
- 상태(State)를 노드 간에 공유 → 앞 에이전트 결과를 다음 에이전트가 받아서 사용
- 조건 분기 가능 (품질 미달 시 재작성 루프 등)

### 왜 LangChain인가?
- Research Agent에서 웹 검색 도구 연결할 때 사용
- DuckDuckGo Search Tool → LangChain Tool로 래핑
- 선행 프로젝트에선 LLM 제거했지만, 이 프로젝트는 웹 검색 + 자료 수집에 활용

### Streamlit이란?
- Python 코드로 웹 UI를 빠르게 만드는 프레임워크
- `streamlit run app.py` 한 줄로 로컬 웹서버 실행
- 무료 배포: streamlit.io/cloud
- HTML/CSS/JS 몰라도 됨

---

## 3. 에이전트별 역할 상세

### Research Agent
```
사용자 입력 (제품명, 카테고리, 키워드)
        ↓
Supabase 건강 DB 조회 (관련 건강 데이터)
        +
DuckDuckGo 웹 검색 (최신 관련 정보)
        ↓
수집한 자료를 구조화된 텍스트로 반환
```
- LangChain의 DuckDuckGo Tool 사용
- Supabase에서 건강 관련 데이터 조회

### Writer Agent
```
Research 결과 + 사용자 입력 (톤앤매너, 타겟)
        ↓
마케팅 블로그 포스팅 생성
- 도입부: 문제 제기 (타겟 고객의 고민)
- 본문: 제품 소개 + 근거 (Research 자료 활용)
- 마무리: CTA (Call To Action)
```
- Python 템플릿 기반 (LLM 비용 없음)
- 톤앤매너에 따라 다른 템플릿 사용

### Image Agent
```
제품명 + 카테고리 + 핵심 키워드
        ↓
Pillow로 이미지 자동 생성
- 배경색: 카테고리별 색상
- 텍스트: 제품명 + 한 줄 소개
- 사이즈: 인스타 정사각형 (1080x1080)
```
- 완전 무료 (Pillow = Python 이미지 라이브러리)
- 인스타그램 발행에 필수

### Publisher Agent
```
생성된 글 + 이미지
        ↓
네이버 블로그  → Selenium (이미 검증됨)
WordPress     → REST API (Application Password)
인스타그램    → instagrapi (개인 계정, 데모용)
```

### Notification Agent
```
발행 완료
        ↓
카카오톡 메시지 또는 슬랙 웹훅
"✅ 발행 완료! 제목: OOO | 네이버 ✅ | WordPress ✅ | 인스타 ✅"
```
- 카카오톡: 카카오 채널 + 비즈니스 메시지 (무료 한도 있음)
- 슬랙: 웹훅 URL로 POST 요청 (완전 무료)

---

## 4. 구현 순서

```
STEP 1: 프로젝트 기본 구조 세팅
  └─ 폴더 구조, requirements.txt, .env.example

STEP 2: Streamlit 웹 UI
  └─ 입력 폼 7개 필드 + 발행 버튼

STEP 3: LangGraph 파이프라인 뼈대
  └─ State 정의, 노드 연결, 워크플로우

STEP 4: Research Agent
  └─ Supabase 건강 DB + DuckDuckGo 검색

STEP 5: Writer Agent
  └─ 마케팅 글 템플릿 + 톤앤매너 분기

STEP 6: Image Agent
  └─ Pillow 이미지 생성

STEP 7: Publisher Agent
  └─ 네이버 (기존 코드 재활용)
  └─ WordPress REST API 연동
  └─ instagrapi 연동

STEP 8: Notification Agent
  └─ 슬랙 웹훅 or 카카오톡

STEP 9: 전체 연결 + 테스트
```

---

## 5. 핵심 기술 개념 정리

### 멀티에이전트란?
- 하나의 큰 작업을 여러 전문 AI(에이전트)가 나눠서 처리
- 각 에이전트는 한 가지 역할만 담당 (단일 책임 원칙)
- 장점: 유지보수 쉬움, 각 에이전트 독립적으로 개선 가능

### 오케스트레이터란?
- 여러 에이전트를 **지휘**하는 역할
- 실행 순서 결정, 상태 전달, 조건 분기 처리
- 이 프로젝트: LangGraph가 오케스트레이터

### LangChain이란?
- LLM(AI 모델)과 각종 도구(검색, DB, API)를 연결하는 프레임워크
- Tool = 에이전트가 사용할 수 있는 기능 단위
- 이 프로젝트: DuckDuckGo 검색 Tool로 웹 검색 자동화

### Streamlit이란?
- Python으로 웹 앱을 만드는 가장 빠른 방법
- 데이터 과학자/AI 개발자용으로 만들어진 프레임워크
- 백엔드 따로 없이 Python 파일 하나로 웹 UI 완성

---

## 6. 멘토 예상 질문 & 답변

**Q. 멀티에이전트를 왜 사용했나요?**
A. 하나의 에이전트가 검색, 글쓰기, 이미지 생성, 발행, 알림을 모두 처리하면 코드가 복잡해지고 유지보수가 어렵습니다. 각 역할을 전담 에이전트로 분리하면 독립적으로 수정·테스트·교체가 가능합니다.

**Q. LangGraph를 오케스트레이터로 선택한 이유는?**
A. LangGraph는 에이전트 간 상태(State)를 그래프 구조로 관리하여 조건 분기와 루프를 명확하게 표현할 수 있습니다. 단순 순차 실행뿐 아니라 "품질 미달 시 재작성" 같은 복잡한 흐름도 쉽게 구현됩니다.

**Q. LangChain은 어디서 사용했나요?**
A. Research Agent에서 DuckDuckGo 검색 Tool을 LangChain으로 래핑하여 사용했습니다. LangChain의 Tool 인터페이스 덕분에 에이전트가 검색 결과를 구조화된 형태로 받아 처리할 수 있습니다.

**Q. 비용을 어떻게 $0으로 유지했나요?**
A. OpenAI 대신 Python 템플릿으로 글을 생성하고, 이미지는 Pillow(무료)로 자동 생성합니다. 발행 플랫폼은 모두 무료 API를 사용하며, 알림은 슬랙 웹훅(무료)으로 처리합니다.

**Q. 인스타그램은 공식 API가 아닌데 괜찮나요?**
A. instagrapi는 비공식 라이브러리로 계정 정지 위험이 있습니다. 이 프로젝트에서는 포트폴리오 데모 목적으로만 사용하며, 실제 서비스에서는 Instagram 비즈니스 계정 + 공식 Graph API 사용을 권장합니다.

**Q. Streamlit을 선택한 이유는?**
A. 마케팅 담당자(비개발자)가 쉽게 사용할 수 있는 UI가 필요했습니다. Streamlit은 Python만으로 직관적인 웹 폼을 빠르게 만들 수 있고, 무료 배포까지 지원합니다.

**Q. 선행 프로젝트(auto-multi-agent)와 다른 점은?**
A. 선행 프로젝트는 DB에서 데이터를 자동으로 가져오는 완전 자동화였습니다. 이 프로젝트는 사용자가 웹에서 제품 정보를 직접 입력하고, LangChain으로 웹 검색까지 수행하며, 이미지 생성과 알림 서비스가 추가된 확장 버전입니다.

**Q. WordPress와 네이버 블로그를 선택한 이유는?**
A. 티스토리는 2023년 API 서비스를 종료했고, dev.to·Hashnode는 개발자 전용 커뮤니티라 건강/마케팅 콘텐츠에 부적합합니다. WordPress는 무료 계정으로 REST API를 사용할 수 있고, 네이버 블로그는 한국 최대 트래픽을 보유해 마케팅에 최적입니다.

**Q. 알림 서비스는 왜 필요한가요?**
A. 자동화 시스템은 사람이 직접 확인하지 않아도 돌아가야 합니다. 발행 완료/실패 시 즉시 알림을 받아야 문제를 빠르게 대응할 수 있습니다. 슬랙 웹훅은 완전 무료로 구현 가능합니다.

---

## 7. 폴더 구조 (예정)

```
health-marketing-agent/
│
├── app.py                   # Streamlit 웹 UI 진입점
│
├── agents/
│   ├── research_agent.py    # 건강 DB + 웹 검색
│   ├── writer_agent.py      # 마케팅 글 생성
│   ├── image_agent.py       # Pillow 이미지 생성
│   ├── publisher_agent.py   # 3개 플랫폼 발행
│   └── notification_agent.py # 카카오/슬랙 알림
│
├── tools/
│   ├── supabase_tools.py    # 건강 DB 조회
│   ├── search_tools.py      # DuckDuckGo 검색
│   ├── naver_tools.py       # 네이버 Selenium
│   ├── wordpress_tools.py   # WordPress REST API
│   └── instagram_tools.py  # instagrapi
│
├── orchestrator/
│   ├── workflow.py          # LangGraph 파이프라인
│   └── state.py             # 공유 상태 정의
│
├── config/
│   └── settings.py          # 환경변수
│
└── docs/
    └── personal_notes.md    # 이 파일 (비공개)
```
