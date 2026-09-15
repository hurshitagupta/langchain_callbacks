import time

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.runnables import RunnableLambda


class LightweightHandler(BaseCallbackHandler):
    raise_error = False

    def __init__(self):
        self.events = 0

    def on_chain_start(self,serialized,inputs,**kwargs):
        self.events += 1

    def on_chain_end(self,outputs,**kwargs,):
        self.events += 1


def create_chain():
    def process(text: str) -> str:
        time.sleep(0.01)
        return f"Processed: {text}"

    return RunnableLambda(process)


def measure_without_callback(chain, runs=20):
    start = time.perf_counter()

    for _ in range(runs):
        chain.invoke("Hello")

    elapsed_ms = (time.perf_counter() - start) * 1000

    return elapsed_ms


def measure_with_callback(chain,handler,runs=20,):
    start = time.perf_counter()

    for _ in range(runs):
        chain.invoke("Hello",
            config={"callbacks": [handler]},
        )

    elapsed_ms = (time.perf_counter() - start) * 1000

    return elapsed_ms


def calculate_overhead(without_callback,with_callback,):
    if without_callback == 0:
        return 0.0

    overhead = ((with_callback - without_callback) / without_callback) * 100

    return overhead


def run_benchmark():
    print("\n=== CALLBACK OVERHEAD BENCHMARK ===")

    chain = create_chain()
    handler = LightweightHandler()

    runs = 20

    without_callback = measure_without_callback(chain,runs)

    with_callback = measure_with_callback(chain,handler,runs)

    overhead = calculate_overhead(without_callback,with_callback)

    print(f"Runs: {runs}")

    print(
        f"Without callback: "
        f"{without_callback:.2f} ms"
    )

    print(
        f"With callback: "
        f"{with_callback:.2f} ms"
    )

    print(
        f"Callback overhead: "
        f"{overhead:.2f}%"
    )

    print(
        f"Callback events recorded: "
        f"{handler.events}"
    )


if __name__ == "__main__":
    run_benchmark()