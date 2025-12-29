from app.nodes.router import router_node
from app.infrastructure import llm


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self, content: str):
        self._content = content

    def invoke(self, *_args, **_kwargs):
        return FakeResponse(self._content)


def test_router_contract_valid_and_invalid_outputs(monkeypatch):
    """
    Contract test:
    The router must always return a valid route and query,
    regardless of whether the LLM output is valid or garbage.
    """

    # Simulate both valid and invalid LLM outputs
    outputs = [
        "PLAN",
        "DIRECT",
        "OFF_TOPIC",
        "nonsense",
        "",
        "123",
    ]

    for output in outputs:
        monkeypatch.setattr(
            llm,
            "get_lightweight_chat_model",
            lambda **_: FakeLLM(output),
        )

        state = {
            "messages": [{"role": "user", "content": "Some input"}],
        }

        result = router_node(state)

        # --- Contract assertions ---
        assert isinstance(result, dict)
        assert "route" in result
        assert "query" in result

        assert result["route"] in {
            "PLAN",
            "DIRECT",
            "OFF_TOPIC",
        }

        assert isinstance(result["query"], str)
