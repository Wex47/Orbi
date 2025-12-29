from __future__ import annotations
from langgraph.graph import StateGraph, START, END
from app.graph.state import State
from app.nodes.router import router_node
from app.nodes.direct import direct_node
from app.nodes.executor import executor_node
from app.nodes.verifier import verifier_node
from app.nodes.finalizer import finalizer_node
from app.nodes.off_topic import off_topic_node
from app.nodes.summarize import build_summarization_node


def build_graph(checkpointer) -> StateGraph[State]:
    """
    Builds the main graph for the travel assistant application.
    inputs: A checkpointer object for state persistence.
    outputs: A compiled StateGraph instance.
    """

    builder = StateGraph(State)
    builder.add_node("summarize", build_summarization_node())
    builder.add_node("router", router_node)
    builder.add_node("direct", direct_node)
    builder.add_node("off_topic", off_topic_node)
    builder.add_node("executor", executor_node)
    builder.add_node("verifier", verifier_node)
    builder.add_node("finalizer", finalizer_node)
    
    builder.add_edge(START, "summarize")
    builder.add_edge("summarize", "router")

    def route_after_router(state: State) -> str:
        return state["route"] or "PLAN"

    builder.add_conditional_edges(
        "router",
        route_after_router,
        {
            "DIRECT": "direct",
            "PLAN": "executor",
            "OFF_TOPIC": "off_topic",
        },
    )

    builder.add_edge("off_topic", "finalizer")
    builder.add_edge("direct", "finalizer")
    builder.add_edge("executor", "verifier")
    builder.add_edge("verifier", "finalizer")
    builder.add_edge("finalizer", END)

    return builder.compile(checkpointer=checkpointer)