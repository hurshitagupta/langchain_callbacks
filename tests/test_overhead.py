from overhead.overhead import LightweightHandler,calculate_overhead,create_chain,measure_with_callback,measure_without_callback


def test_overhead_measurement_success():
    chain = create_chain()
    handler = LightweightHandler()

    runs = 3

    without_callback = measure_without_callback(chain, runs)

    with_callback = measure_with_callback(chain, handler, runs)

    overhead = calculate_overhead(without_callback,with_callback,)

    assert without_callback > 0
    assert with_callback > 0

    assert handler.events == runs * 2

    assert isinstance(overhead, float)


def test_overhead_zero_baseline():
    overhead = calculate_overhead( 0,100)

    assert overhead == 0.0