from app.nodes.verifier import verifier_node


# ============================================================
# Test helpers (fake LLM)
# ============================================================

class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self, content: str):
        self._content = content

    def invoke(self, *_args, **_kwargs):
        return FakeResponse(self._content)


# ============================================================
# Contract test
# ============================================================

def test_verifier_node_contract(monkeypatch):
    """
    Contract test:
    The verifier node must always return a dict with a boolean `verified`,
    regardless of whether the LLM verdict is VERIFIED or INVALID.
    """

    verdicts = [
        "VERIFIED",
        "INVALID: unsupported claim",
        "INVALID: contradiction",
        "",
        "SOME GARBAGE OUTPUT",
    ]

    for verdict in verdicts:
        monkeypatch.setattr(
            "app.nodes.verifier.get_lightweight_chat_model",
            lambda **_: FakeLLM(verdict),
        )

        state = {
            "query": "Is Rome worth visiting?",
            "execution": "Rome is great.",
            "messages": [],
        }

        result = verifier_node(state)

        # --- Contract guarantees ---
        assert isinstance(result, dict)
        assert "verified" in result
        assert isinstance(result["verified"], bool)


# ============================================================
# Unit tests (specific behavior)
# ============================================================

def test_verifier_marks_verified(monkeypatch):
    monkeypatch.setattr(
        "app.nodes.verifier.get_lightweight_chat_model",
        lambda **_: FakeLLM("VERIFIED"),
    )

    state = {
        "query": "Is Rome worth visiting?",
        "execution": "Rome is great.",
        "messages": [],
    }

    result = verifier_node(state)

    assert result["verified"] is True


def test_verifier_marks_invalid(monkeypatch):
    monkeypatch.setattr(
        "app.nodes.verifier.get_lightweight_chat_model",
        lambda **_: FakeLLM("INVALID: hallucination"),
    )

    state = {
        "query": "Is Rome worth visiting?",
        "execution": "Rome is on Mars.",
        "messages": [],
    }

    result = verifier_node(state)

    assert result["verified"] is False


def test_verifier_invalid_on_unexpected_output(monkeypatch):
    """
    Any output not starting with VERIFIED should be treated as invalid.
    """

    monkeypatch.setattr(
        "app.nodes.verifier.get_lightweight_chat_model",
        lambda **_: FakeLLM("MAYBE"),
    )

    state = {
        "query": "Is Rome worth visiting?",
        "execution": "Rome is nice.",
        "messages": [],
    }

    result = verifier_node(state)

    assert result["verified"] is False