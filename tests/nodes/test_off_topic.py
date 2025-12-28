from app.nodes.off_topic import off_topic_node


def test_off_topic_contract():
    """
    Contract test:
    The off-topic node must always return a deterministic refusal,
    mark the response as verified, and never indicate tool usage.
    """

    # Input content should not matter
    state_variants = [
        {},
        {"messages": []},
        {"messages": ["random input"]},
        {"messages": [{"role": "user", "content": "Tell me a joke"}]},
    ]

    for state in state_variants:
        result = off_topic_node(state)

        assert isinstance(result, dict)

        # Contract guarantees
        assert "execution" in result
        assert "verified" in result
        assert "tools_used" in result

        assert isinstance(result["execution"], str)
        assert result["verified"] is True
        assert result["tools_used"] is False