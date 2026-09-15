import os
import time

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openrouter import ChatOpenRouter

load_dotenv()


class MetricsHandler(BaseCallbackHandler):
    raise_error = False

    def __init__(self):
        self.metrics = {}
        self.start_times = {}

    def on_llm_start(self,serialized,prompts,*,run_id,**kwargs):
        self.start_times[run_id] = time.perf_counter()

        self.metrics[run_id] = {
            "tokens": 0,
            "latency_ms": 0,
            "errors": 0,
        }

        print(f"[LLM START] run_id={run_id}")

    def on_llm_end(self,response,*,run_id,**kwargs):
        start_time = self.start_times.pop(run_id,time.perf_counter())

        latency_ms = (time.perf_counter() - start_time) * 1000

        token_usage = {}

        if response.llm_output:
            token_usage = response.llm_output.get("token_usage",{})

        total_tokens = token_usage.get("total_tokens",0)

        self.metrics[run_id]["tokens"] = total_tokens
        self.metrics[run_id]["latency_ms"] = round(latency_ms,2)

        print(f"[LLM END] run_id={run_id}")
        print(f"Tokens: {total_tokens}")
        print(f"Latency: {latency_ms:.2f} ms")

    def on_llm_error(self,error,*,run_id,**kwargs):
        if run_id not in self.metrics:
            self.metrics[run_id] = {"tokens": 0,"latency_ms": 0,"errors": 0}

        self.metrics[run_id]["errors"] += 1

        self.start_times.pop(run_id, None)

        print(f"[LLM ERROR] run_id={run_id}")
        print(f"Error: {error}")


def get_model():
    return ChatOpenRouter(
        model=os.getenv("MODEL_NAME"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("BASE_URL"),
        temperature=0,
        timeout=20_000,
        max_retries=2,
    )


def run_success_case():
    print("\n=== SUCCESS CASE ===")

    handler = MetricsHandler()
    model = get_model()

    response = model.invoke(
        "Explain callbacks in one short sentence.",
        config={"callbacks": [handler]},
    )

    print("\nModel response:")
    print(response.content)

    print("\nMetrics:")

    for run_id, data in handler.metrics.items():
        print(f"Run ID: {run_id}")
        print(f"Tokens: {data['tokens']}")
        print(f"Latency: {data['latency_ms']} ms")
        print(f"Errors: {data['errors']}")


def run_failure_case():
    print("\n=== FAILURE CASE ===")

    handler = MetricsHandler()

    demo_run_id = "failed-run-001"

    handler.on_llm_error(RuntimeError("Demo LLM failure"),run_id=demo_run_id)

    print("\nFailure metrics:")
    print(handler.metrics[demo_run_id])


if __name__ == "__main__":
    run_success_case()
    run_failure_case()