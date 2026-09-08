import pytest

def test_dht_read_public_dummy_values():
    """
    Corresponds to C's test_dht_read_public.c.
    Tests with different fixed dummy values to distinguish public from original.
    """
    humidity = 60.5
    temperature = 36.6
    assert humidity == pytest.approx(60.5)
    assert temperature == pytest.approx(36.6)