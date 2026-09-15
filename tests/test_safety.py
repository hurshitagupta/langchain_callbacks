from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.runnables import RunnableLambda


class ThrowingChainHandler(BaseCallbackHandler):
    raise_error = False

    def __init__(self):
        self.callback_attempted = False

    def on_chain_start( self, serialized,inputs,**kwargs):
        self.callback_attempted = True
        raise RuntimeError("Intentional callback failure")


def test_throwing_handler_does_not_break_chain():
    handler = ThrowingChainHandler()

    chain = RunnableLambda(lambda text: f"Processed: {text}")

    result = chain.invoke("Hello",config={"callbacks": [handler]})

    assert handler.callback_attempted is True

    assert result == "Processed: Hello"


def test_chain_without_handler():
    chain = RunnableLambda(lambda text: f"Processed: {text}")

    result = chain.invoke("Hello")

    assert result == "Processed: Hello"