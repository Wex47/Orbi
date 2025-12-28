from app.graph.graph import build_graph
from app.graph.state import State

"""Verify graph routing and state propagation using deterministic fake nodes, without invoking LLMs or external tools."""


# ------------------------------------------------------------
# Helpers: fake nodes
# ------------------------------------------------------------

def fake_summarize(state: State) -> State:
    state["context"] = {"summary": "ok"}
    return state


def fake_router_plan(state: State) -> State:
    state["route"] = "PLAN"
    state["query"] = "plan trip"
    return state


def fake_router_direct(state: State) -> State:
    state["route"] = "DIRECT"
    state["query"] = "direct answer"
    return state


def fake_router_off_topic(state: State) -> State:
    state["route"] = "OFF_TOPIC"
    state["query"] = "irrelevant"
    return state


def fake_executor(state: State) -> State:
    state["execution"] = "executed"
    state["tools_used"] = True
    return state


def fake_verifier(state: State) -> State:
    state["verified"] = True
    return state


def fake_direct(state: State) -> State:
    state["execution"] = "direct"
    state["tools_used"] = False
    return state


def fake_off_topic(state: State) -> State:
    state["final_answer"] = "off topic response"
    return state


def fake_finalizer(state: State) -> State:
    state["final_answer"] = "final answer"
    return state


# ------------------------------------------------------------
# PLAN path
# ------------------------------------------------------------

def test_graph_plan_path(monkeypatch):
    monkeypatch.setattr(
        "app.graph.graph.build_summarization_node",
        lambda: fake_summarize,
    )
    monkeypatch.setattr(
        "app.graph.graph.router_node",
        fake_router_plan,
    )
    monkeypatch.setattr(
        "app.graph.graph.executor_node",
        fake_executor,
    )
    monkeypatch.setattr(
        "app.graph.graph.verifier_node",
        fake_verifier,
    )
    monkeypatch.setattr(
        "app.graph.graph.finalizer_node",
        fake_finalizer,
    )

    graph = build_graph(checkpointer=None)

    initial_state: State = {
        "messages": [],
    }

    result = graph.invoke(initial_state)

    assert result["route"] == "PLAN"
    assert result["execution"] == "executed"
    assert result["tools_used"] is True
    assert result["verified"] is True
    assert result["final_answer"] == "final answer"


# ------------------------------------------------------------
# DIRECT path
# ------------------------------------------------------------

def test_graph_direct_path(monkeypatch):
    monkeypatch.setattr(
        "app.graph.graph.build_summarization_node",
        lambda: fake_summarize,
    )
    monkeypatch.setattr(
        "app.graph.graph.router_node",
        fake_router_direct,
    )
    monkeypatch.setattr(
        "app.graph.graph.direct_node",
        fake_direct,
    )
    monkeypatch.setattr(
        "app.graph.graph.finalizer_node",
        fake_finalizer,
    )

    graph = build_graph(checkpointer=None)

    initial_state: State = {
        "messages": [],
    }

    result = graph.invoke(initial_state)

    assert result["route"] == "DIRECT"
    assert result["execution"] == "direct"
    assert result["tools_used"] is False
    assert result["final_answer"] == "final answer"


# ------------------------------------------------------------
# OFF_TOPIC path
# ------------------------------------------------------------

def test_graph_off_topic_path(monkeypatch):
    monkeypatch.setattr(
        "app.graph.graph.build_summarization_node",
        lambda: fake_summarize,
    )
    monkeypatch.setattr(
        "app.graph.graph.router_node",
        fake_router_off_topic,
    )
    monkeypatch.setattr(
        "app.graph.graph.off_topic_node",
        fake_off_topic,
    )
    monkeypatch.setattr(
        "app.graph.graph.finalizer_node",
        fake_finalizer,
    )

    graph = build_graph(checkpointer=None)

    initial_state: State = {
        "messages": [],
    }

    result = graph.invoke(initial_state)

    assert result["route"] == "OFF_TOPIC"
    assert result["final_answer"] == "final answer"
