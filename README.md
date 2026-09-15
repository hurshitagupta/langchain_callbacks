# Callbacks

This project implements LangChain callbacks for observing model, tool, and chain lifecycle events without changing the behaviour of the underlying chain.

## Task 1 — Custom Handler

Task 1 implements a custom LangChain callback handler using `BaseCallbackHandler`.

The handler covers the following lifecycle hooks:

- `on_llm_start` — triggered when an LLM call starts.
- `on_llm_end` — triggered when an LLM call completes successfully.
- `on_llm_error` — records an LLM failure.
- `on_tool_start` — triggered when a tool starts.
- `on_tool_end` — triggered when a tool finishes.
- `on_chain_error` — records a chain failure.

The handler stores each callback event in an `events` list, making the lifecycle easy to inspect and test.

### Implementation

The success case performs a real model invocation using `ChatOpenRouter` and invokes a simple calculator tool.

The callback handler is attached using:

```python
config={"callbacks": [handler]}
```

LangChain automatically triggers the appropriate LLM and tool lifecycle callbacks.

A controlled failure case is also included to demonstrate the LLM and chain error handlers.

### Run Task 1

```bash
uv run python -m custom_handler.custom_handler
```

### Automated Tests

Run the tests with:

```bash
uv run pytest tests/test_custom_handler.py -v
```

### Evidence

Execution and test outputs can be saved using:

```bash
uv run python -m custom_handler.custom_handler > outputs/custom_handler.txt

uv run pytest tests/test_custom_handler.py -v > outputs/test_custom_handler.txt
```

### Task 1 Status

- Custom `BaseCallbackHandler` implemented
- LLM start/end/error callbacks implemented
- Tool start/end callbacks implemented
- Chain error callback implemented
- Real LLM and tool lifecycle demonstrated
- Success and failure cases demonstrated
- Automated tests added