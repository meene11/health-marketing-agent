from langgraph.graph import StateGraph, END
from orchestrator.state import MarketingState


def research_node(state: MarketingState) -> MarketingState:
    from agents.research_agent import run_research
    print("\n[1/4] Research Agent - 자료 수집 중...")
    result = run_research(
        product_name=state["product_name"],
        category=state["category"],
        strengths=state["strengths"],
    )
    return {**state, "research_result": result}


def write_node(state: MarketingState) -> MarketingState:
    from agents.writer_agent import run_writer
    print("\n[2/4] Writer Agent - 마케팅 글 작성 중...")
    result = run_writer(
        product_name=state["product_name"],
        category=state["category"],
        intro=state["intro"],
        strengths=state["strengths"],
        target=state["target"],
        tone=state["tone"],
        research_result=state["research_result"],
    )
    return {**state, "title": result["title"], "content": result["content"]}


def image_node(state: MarketingState) -> MarketingState:
    from agents.image_agent import run_image_agent
    print("\n[3/4] Image Agent - 이미지 생성 중...")
    image_path = run_image_agent(
        product_name=state["product_name"],
        category=state["category"],
        intro=state["intro"],
    )
    return {**state, "image_path": image_path}


def publish_node(state: MarketingState) -> MarketingState:
    from agents.publisher_agent import run_publisher
    print("\n[4/4] Publisher Agent - 발행 중...")
    results = run_publisher(
        title=state["title"],
        content=state["content"],
        image_path=state.get("image_path", ""),
        strengths=state["strengths"],
        intro=state["intro"],
        tone=state["tone"],
        platforms=state["platforms"],
    )
    return {**state, "published_urls": results}


def notify_node(state: MarketingState) -> MarketingState:
    from agents.notification_agent import run_notification
    print("\n[완료] Notification Agent - 슬랙 알림 중...")
    run_notification(title=state["title"], published_urls=state["published_urls"])
    return state


def build_workflow() -> StateGraph:
    graph = StateGraph(MarketingState)

    graph.add_node("research", research_node)
    graph.add_node("write", write_node)
    graph.add_node("image", image_node)
    graph.add_node("publish", publish_node)
    graph.add_node("notify", notify_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "write")
    graph.add_edge("write", "image")
    graph.add_edge("image", "publish")
    graph.add_edge("publish", "notify")
    graph.add_edge("notify", END)

    return graph.compile()


def run_pipeline(user_input: dict) -> MarketingState:
    workflow = build_workflow()

    initial_state: MarketingState = {
        "product_name": user_input["product_name"],
        "category": user_input["category"],
        "intro": user_input["intro"],
        "strengths": user_input["strengths"],
        "target": user_input["target"],
        "tone": user_input["tone"],
        "platforms": user_input["platforms"],
        "research_result": "",
        "title": "",
        "content": "",
        "image_path": "",
        "published_urls": {},
    }

    return workflow.invoke(initial_state)
