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

---

## Task 3 — Scoped Attach

Task 3 demonstrates how callback handlers can be attached to individual LangChain invocations instead of being configured globally.

The callback is passed through the invocation configuration:

```python
config={"callbacks": [handler]}
```

This means the handler observes only the invocation where it is explicitly attached.

### Implementation

Two model invocations are performed.

The first invocation attaches the callback:

```python
response1 = model.invoke(
    "Reply with only the word: Hello",
    config={"callbacks": [handler]},
)
```

The second invocation does not attach the callback:

```python
response2 = model.invoke(
    "Reply with only the word: Hi"
)
```

The number of recorded events is compared before and after the second invocation.

If the event count remains unchanged, it proves that the callback was scoped only to the first invocation.

### Run Task 3

```bash
uv run python -m scoped_attach.scoped_attach
```

### Automated Tests

Run:

```bash
uv run pytest tests/test_scoped_attach.py -v
```

### Save Evidence

```bash
uv run python -m scoped_attach.scoped_attach > outputs/scoped_attach.txt

uv run pytest tests/test_scoped_attach.py -v > outputs/test_scoped_attach.txt
```

---

## Task 4 — Safety

Task 4 demonstrates that a failure inside a callback handler does not break the main LangChain execution.

Callbacks are generally used for side effects such as logging, tracing and metrics. A failure in one of these side effects should not prevent the main chain from completing.

### Throwing Handler

A custom callback handler intentionally raises an exception:

```python
class ThrowingHandler(BaseCallbackHandler):
    raise_error = False

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.callback_attempted = True

        raise RuntimeError(
            "Intentional callback failure"
        )
```

The handler uses:

```python
raise_error = False
```

so the callback exception is handled without propagating it as the main chain failure.

### Safety Demonstration

The throwing callback is attached to the model using invocation configuration:

```python
response = model.invoke(
    "Reply with only the word SAFE",
    config={"callbacks": [handler]},
)
```

The callback intentionally fails during `on_llm_start`, but the model invocation is still allowed to complete.

The `callback_attempted` flag is used to prove that the callback actually executed before throwing the exception.

### Run Task 4

```bash
uv run python -m safety.safety
```

### Automated Tests

Run:

```bash
uv run pytest tests/test_safety.py -v
```

### Save Evidence

Save the main execution:

```bash
uv run python -m safety.safety > outputs/safety.txt 2>&1
```

Save the automated test output:

```bash
uv run pytest tests/test_safety.py -v > outputs/test_safety.txt 2>&1
```

---

## Task 5 — Callback Overhead

Task 5 measures the performance overhead introduced by attaching a callback handler to a LangChain runnable.

The same controlled workload is executed:

1. Without a callback
2. With a callback

Both execution times are measured in milliseconds and the callback overhead is reported as a percentage.

### Benchmark

A local `RunnableLambda` is used instead of an external LLM API.

This avoids network and provider latency affecting the callback measurement.

The runnable performs a small fixed workload:

```python
def process(text: str) -> str:
    time.sleep(0.01)
    return f"Processed: {text}"
```

A lightweight callback records the chain start and end events.

### Overhead Calculation

Callback overhead is calculated using:

```python
overhead = (
    (with_callback - without_callback)
    / without_callback
) * 100
```

The benchmark executes the runnable 20 times in each configuration to reduce the effect of measuring only a single execution.

### Run Task 5

```bash
uv run python -m overhead.overhead
```

### Automated Tests

Run:

```bash
uv run pytest tests/test_overhead.py -v
```

### Save Evidence

Save benchmark output:

```bash
uv run python -m overhead.overhead > outputs/overhead.txt
```

Save automated test output:

```bash
uv run pytest tests/test_overhead.py -v > outputs/test_overhead.txt
```

---

## Guardrails and Evidence

The project includes shared guardrails to prevent uncontrolled execution and oversized inputs during the assessment.

The main guardrail logic is stored in:

```text
guardrails.py
```

Evidence for the implemented guardrails is generated using:

```text
guardrails_evidence.py
```

This evidence file intentionally triggers the guardrails so their behaviour can be demonstrated and saved as part of the 

### Shared Guardrail Design

The guardrails are kept in a shared module rather than rewriting the same checks separately for every task.

The implemented guardrail evidence demonstrates:

* Hard step limit
* Per-operation timeout
* Capped retry attempts
* Input/token budget enforcement

### Run Guardrail Evidence

```bash
uv run python guardrails_evidence.py
```

### Save Guardrail Evidence

```bash
uv run python guardrails_evidence.py > outputs/guardrails_evidence.txt
```

The saved output provides reproducible evidence that each guardrail fires when its configured limit or failure condition is reached.

---

## Environment Configuration

The project uses environment variables to keep API credentials and model configuration outside the source code.

An `.env.example` file is included to show the required environment variables without exposing any actual secrets:

Create a local `.env` file using the same variables and provide your own values.

The actual `.env` file is excluded from GitHub using `.gitignore` to ensure that API keys are not committed to the repository.

## Requirements

The `requirements.txt` file contains the Python dependencies required to run the assessment.

Install the dependencies using:

```bash
uv pip install -r requirements.txt
```

The main dependencies used in this assessment include LangChain, OpenRouter integration, FastAPI, Uvicorn, python-dotenv, HTTPX, and pytest.

After installing the dependencies and configuring the `.env` file, the individual assessment tasks can be executed using the commands provided in their respective sections above.