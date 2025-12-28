from app.nodes.finalizer import finalizer_node


# ============================================================
# Contract tests
# ============================================================

def test_finalizer_contract_valid_and_edge_cases():
    """
    Contract test:
    The finalizer must always return a final_answer string and append
    exactly one assistant message, regardless of input state.
    """

    test_states = [
        {},  # no inputs at all
        {"execution": "Answer"},
        {"execution": "Answer", "verified": True},
        {"execution": "Answer", "tools_used": True},
        {"execution": "Answer", "verified": True, "tools_used": True},
        {"execution": "", "verified": False, "tools_used": False},
        {"execution": "Direct", "route": "DIRECT"},
    ]

    for state in test_states:
        result = finalizer_node(state)

        # --- Contract guarantees ---
        assert isinstance(result, dict)

        assert "final_answer" in result
        assert "messages" in result

        assert isinstance(result["final_answer"], str)
        assert isinstance(result["messages"], list)
        assert len(result["messages"]) == 1

        message = result["messages"][0]
        assert message["role"] == "assistant"
        assert message["content"] == result["final_answer"]


# ============================================================
# Unit tests (specific behavior)
# ============================================================

def test_finalizer_no_warnings_when_verified_and_grounded():
    state = {
        "execution": "Here is the answer",
        "verified": True,
        "tools_used": True,
        "route": "PLAN",
    }

    result = finalizer_node(state)

    assert result["final_answer"] == "Here is the answer"


def test_finalizer_adds_verification_warning():
    state = {
        "execution": "Answer",
        "verified": False,
        "tools_used": True,
        "route": "PLAN",
    }

    result = finalizer_node(state)

    assert "could not be fully verified" in result["final_answer"]


def test_finalizer_adds_grounding_warning_when_no_tools():
    state = {
        "execution": "Answer",
        "verified": True,
        "tools_used": False,
        "route": "PLAN",
    }

    result = finalizer_node(state)

    assert "not grounded in tool invocation" in result["final_answer"]


def test_finalizer_adds_grounding_warning_on_direct_route():
    state = {
        "execution": "Direct answer",
        "verified": True,
        "tools_used": True,
        "route": "DIRECT",
    }

    result = finalizer_node(state)

    assert "not grounded in tool invocation" in result["final_answer"]


def test_finalizer_combines_multiple_warnings():
    state = {
        "execution": "Answer",
        "verified": False,
        "tools_used": False,
        "route": "PLAN",
    }

    result = finalizer_node(state)

    final = result["final_answer"]

    assert "could not be fully verified" in final
    assert "not grounded in tool invocation" in final
    assert "---" in final
