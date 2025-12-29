from app.nodes.direct import direct_node

# ============================================================
# Contract test
# ============================================================

class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self, content: str):
        self._content = content

    def invoke(self, *_args, **_kwargs):
        return FakeResponse(self._content)


def test_direct_node_contract(monkeypatch):
    """
    Contract test:
    The direct node must always return an execution string
    and mark the result as unverified, regardless of LLM output.
    """

    outputs = [
        "Simple travel advice",
        "",
        "Here are some tips for visiting Rome.",
    ]

    for output in outputs:
        monkeypatch.setattr(
            "app.nodes.direct.get_lightweight_chat_model",
            lambda **_: FakeLLM(output),
        )

        state = {
            "messages": [{"role": "user", "content": "Tell me about Rome"}],
        }

        result = direct_node(state)

        # --- Contract guarantees ---
        assert isinstance(result, dict)
        assert "execution" in result
        assert "verified" in result

        assert isinstance(result["execution"], str)
        assert result["verified"] is False


# ============================================================
# Unit test (basic behavior)
# ============================================================

def test_direct_node_returns_llm_response(monkeypatch):
    monkeypatch.setattr(
        "app.nodes.direct.get_lightweight_chat_model",
        lambda **_: FakeLLM("Direct answer"),
    )

    state = {
        "messages": [{"role": "user", "content": "Is Rome worth visiting?"}],
    }

    result = direct_node(state)

    assert result["execution"] == "Direct answer"
    assert result["verified"] is False