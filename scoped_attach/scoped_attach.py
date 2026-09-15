import os

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openrouter import ChatOpenRouter

load_dotenv()


class ScopedHandler(BaseCallbackHandler):
    raise_error = False

    def __init__(self):
        self.events = []

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.events.append("llm_start")
        print("[CALLBACK] LLM started")

    def on_llm_end(self, response, **kwargs):
        self.events.append("llm_end")
        print("[CALLBACK] LLM ended")

    def on_llm_error(self, error, **kwargs):
        self.events.append("llm_error")
        print(f"[CALLBACK] LLM error: {error}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        self.events.append("chain_start")
        print("[CALLBACK] Chain started")

    def on_chain_end(self, outputs, **kwargs):
        self.events.append("chain_end")
        print("[CALLBACK] Chain ended")


def get_model():
    return ChatOpenRouter(
        model=os.getenv("MODEL_NAME"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("BASE_URL"),
        temperature=0,
        timeout=20_000,
        max_retries=2,
    )


def run_demo():
    model = get_model()
    handler = ScopedHandler()

    print("\n=== INVOCATION 1: CALLBACK ATTACHED ===")

    response1 = model.invoke(
        "Reply with only the word: Hello",
        config={"callbacks": [handler]},
    )

    print("Response:", response1.content)
    print("Events:", handler.events)

    first_run_event_count = len(handler.events)

    print("\n=== INVOCATION 2: NO CALLBACK ATTACHED ===")

    response2 = model.invoke(
        "Reply with only the word: Hi"
    )

    print("Response:", response2.content)
    print("Events:", handler.events)

    second_run_event_count = len(handler.events)

    print("\n=== SCOPED ATTACH RESULT ===")

    print(
        "Events after invocation 1:",
        first_run_event_count,
    )

    print(
        "Events after invocation 2:",
        second_run_event_count,
    )

    if first_run_event_count == second_run_event_count:
        print(
            "PASS: Second invocation did not use the callback."
        )
    else:
        print(
            "FAIL: Callback was triggered unexpectedly."
        )


if __name__ == "__main__":
    run_demo()