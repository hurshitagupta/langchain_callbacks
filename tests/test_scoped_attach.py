from langchain_core.runnables import RunnableLambda

from scoped_attach.scoped_attach import ScopedHandler


def test_callback_is_scoped_to_invocation():
    handler = ScopedHandler()

    chain = RunnableLambda(lambda text: f"Response: {text}")

    chain.invoke("Hello", config={"callbacks": [handler]})

    events_after_first_run = len(handler.events)

    chain.invoke("Hi")

    events_after_second_run = len(handler.events)

    assert events_after_first_run > 0
    assert events_after_second_run == events_after_first_run


def test_handler_not_attached():
    handler = ScopedHandler()

    chain = RunnableLambda(lambda text: f"Response: {text}")

    result = chain.invoke("Hello")

    assert result == "Response: Hello"
    assert handler.events == []