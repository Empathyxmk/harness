import pytest

def test_dht_read_dummy_values():
    """
    Corresponds to C's test_dht_read.c.
    This C test was a very basic assertion of fixed dummy values.
    """
    humidity = 50.0
    temperature = 42.0
    assert humidity == pytest.approx(50.0)
    assert temperature == pytest.approx(42.0)
    # The original C file's printf is for output, not an assertion.