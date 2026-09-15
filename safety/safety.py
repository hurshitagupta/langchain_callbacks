import os

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openrouter import ChatOpenRouter

load_dotenv()


class ThrowingHandler(BaseCallbackHandler):

    raise_error = False

    def __init__(self):
        self.callback_attempted = False

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.callback_attempted = True

        print("[CALLBACK] Handler started")
        print("[CALLBACK] Intentionally throwing an error...")

        raise RuntimeError(
            "Intentional callback failure"
        )


def get_model():
    return ChatOpenRouter(
        model=os.getenv("MODEL_NAME"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("BASE_URL"),
        temperature=0,
        timeout=20_000,
        max_retries=2,
    )


def run_safety_demo():
    print("\n=== CALLBACK SAFETY TEST ===")

    handler = ThrowingHandler()
    model = get_model()

    try:
        response = model.invoke(
            "Reply with only the word SAFE",
            config={"callbacks": [handler]},
        )

        print("\nModel response:")
        print(response.content)

        print(
            "\nCallback attempted:",
            handler.callback_attempted,
        )

        print(
            "PASS: Chain completed even though "
            "the callback raised an exception."
        )

    except Exception as error:
        print("\nFAIL: Chain was broken.")
        print("Error:", error)


if __name__ == "__main__":
    run_safety_demo()