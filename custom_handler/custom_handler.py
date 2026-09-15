import os

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tools import tool
from langchain_openrouter import ChatOpenRouter

load_dotenv()


class CustomHandler(BaseCallbackHandler):
    raise_error = False

    def __init__(self):
        self.events = []

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.events.append("llm_start")
        print("[LLM START]")

    def on_llm_end(self, response, **kwargs):
        self.events.append("llm_end")
        print("[LLM END]")

    def on_llm_error(self, error, **kwargs):
        self.events.append("llm_error")
        print(f"[LLM ERROR] {error}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown")
        self.events.append("tool_start")
        print(f"[TOOL START] {tool_name}")

    def on_tool_end(self, output, **kwargs):
        self.events.append("tool_end")
        print(f"[TOOL END] {output}")

    def on_chain_error(self, error, **kwargs):
        self.events.append("chain_error")
        print(f"[CHAIN ERROR] {error}")


@tool
def calculator(expression: str) -> str:
    """Evaluate a simple multiplication expression."""
    left, right = expression.split("*")
    return str(float(left.strip()) * float(right.strip()))


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

    handler = CustomHandler()
    model = get_model()

    response = model.invoke(
        "Say hello in one short sentence.",
        config={"callbacks": [handler]},
    )

    print("Model response:", response.content)

    tool_result = calculator.invoke(
        {"expression": "45 * 23"},
        config={"callbacks": [handler]},
    )

    print("Calculator result:", tool_result)

    print("\nEvents captured:")
    print(handler.events)


def run_failure_case():
    print("\n=== FAILURE CASE ===")

    handler = CustomHandler()
    
    handler.on_llm_error(RuntimeError("Demo LLM failure"))
    handler.on_chain_error(RuntimeError("Demo chain failure"))

    print("\nFailure events captured:")
    print(handler.events)


if __name__ == "__main__":
    run_success_case()
    run_failure_case()