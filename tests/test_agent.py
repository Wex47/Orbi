def test_agent_uses_climate_tool(agent_executor):
    response = agent_executor.invoke(
        {
            "input": "What is the weather in Rome in April?",
            "chat_history": [],
        }
    )

    steps = response.get("intermediate_steps", [])
    tool_names = [step[0].tool for step in steps]
    print(response)
    print(tool_names)
    assert "get_place_climate" in tool_names
