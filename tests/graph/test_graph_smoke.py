import pytest
from app.graph.graph import build_graph

"""End-to-end smoke test to ensure the graph executes successfully with real components and produces a reasonable final response."""

@pytest.mark.external
def test_travel_graph_smoke():
    graph = build_graph(checkpointer=None)
    result = graph.invoke(
        {"messages": ["Do you recommend visiting Rome? what are the best sights to see?"]}
    )

    assert "messages" in result
    assert len(result["messages"]) > 0

    final_text = result["messages"][-1].content.lower()
    assert "rome" in final_text
