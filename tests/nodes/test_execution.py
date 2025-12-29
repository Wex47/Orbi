from langchain_core.messages import ToolMessage
from app.nodes.executor import executor_node


class FakeAgent:
    def __init__(self, messages):
        self._messages = messages

    def invoke(self, *_args, **_kwargs):
        return {"messages": self._messages}


def test_executor_contract_valid_and_edge_cases(monkeypatch):
    """
    Contract test:
    The executor must always return a string 'execution' and a boolean
    'tools_used', regardless of tool usage or message structure.
    """

    test_cases = [
        # No messages
        [],
        # Assistant-only message (dict)
        [{"role": "assistant", "content": "Hello"}],
        # Tool message (dict form)
        [{"role": "tool", "content": "Tool output"}],
        # ToolMessage object (correct schema)
        [
            ToolMessage(
                content="Tool output",
                tool_call_id="test-tool-call",
            )
        ],
        # Mixed messages
        [
            {"role": "assistant", "content": "Thinking"},
            {"role": "tool", "content": "Tool output"},
            {"role": "assistant", "content": "Final answer"},
        ],
    ]

    for messages in test_cases:
        monkeypatch.setattr(
            "app.nodes.executor._get_agent",
            lambda: FakeAgent(messages),
        )

        state = {"messages": ["user input"]}

        result = executor_node(state)

        # Contract assertions
        assert isinstance(result, dict)
        assert "execution" in result
        assert "tools_used" in result
        assert isinstance(result["execution"], str)
        assert isinstance(result["tools_used"], bool)
