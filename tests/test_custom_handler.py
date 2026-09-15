from custom_handler.custom_handler import CustomHandler


def test_success_callbacks():
    handler = CustomHandler()

    handler.on_llm_start({}, ["Hello"])
    handler.on_llm_end(None)

    handler.on_tool_start({"name": "calculator"}, "45 * 23")
    handler.on_tool_end("1035.0")

    assert handler.events == ["llm_start","llm_end","tool_start","tool_end"]


def test_failure_callbacks():
    handler = CustomHandler()

    handler.on_llm_error(RuntimeError("Demo LLM failure"))
    handler.on_chain_error(RuntimeError("Demo chain failure"))

    assert handler.events == ["llm_error","chain_error"]