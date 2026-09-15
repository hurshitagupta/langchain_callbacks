from uuid import uuid4

from langchain_core.outputs import Generation, LLMResult

from metrics.metrics import MetricsHandler


def test_metrics_success():
    handler = MetricsHandler()
    run_id = uuid4()

    handler.on_llm_start({},["Hello"],run_id=run_id)

    response = LLMResult(
        generations=[
            [Generation(text="Hello!")]
        ],
        llm_output={"token_usage": {"total_tokens": 25}}
    )

    handler.on_llm_end(response,run_id=run_id,)

    metrics = handler.metrics[run_id]

    assert metrics["tokens"] == 25
    assert metrics["latency_ms"] >= 0
    assert metrics["errors"] == 0


def test_metrics_failure():
    handler = MetricsHandler()
    run_id = uuid4()

    handler.on_llm_start( {},["Hello"],run_id=run_id)

    handler.on_llm_error(RuntimeError("Test LLM failure"),run_id=run_id)

    metrics = handler.metrics[run_id]

    assert metrics["tokens"] == 0
    assert metrics["errors"] == 1