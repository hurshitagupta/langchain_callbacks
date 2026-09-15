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

---

## Task 2 — Metrics

Task 2 extends the callback handler to collect metrics for each LLM execution.

The following metrics are recorded per `run_id`:

- Total token usage
- LLM latency in milliseconds
- Error count

Each LangChain LLM execution receives a unique `run_id`, which is used to keep the metrics for different runs separate.

### Metrics Structure

Metrics are stored in the following format:

```python
{
    run_id: {
        "tokens": 25,
        "latency_ms": 850.42,
        "errors": 0
    }
}
```

### Latency Measurement

When the LLM starts, the callback stores the start time using `time.perf_counter()`.

When the LLM finishes, the elapsed time is calculated and converted to milliseconds.

```python
latency_ms = (
    time.perf_counter() - start_time
) * 1000
```

### Token Usage

Token usage is extracted from the LLM response metadata and stored against the corresponding `run_id`.

If token usage is unavailable, the handler safely defaults the value to `0`.

### Error Count

`on_llm_error` increments the error count for the corresponding run.

This allows successful and failed LLM executions to be measured separately.

### Run Task 2

```bash
uv run python -m task2_metrics.metrics
```

### Automated Tests

Run:

```bash
uv run pytest tests/test_metrics.py -v
```

### Save Evidence

```bash
uv run python -m metrics.metrics > outputs/metrics.txt

uv run pytest tests/test_metrics.py -v > outputs/test_metrics.txt
```