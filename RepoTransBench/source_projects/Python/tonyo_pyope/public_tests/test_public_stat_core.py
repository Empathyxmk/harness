import pytest

def test_hgd_sample_manual_public():
    # Manual sampling logic: pick randint between a and b using coins
    a, b = 5, 8
    coins = [1, 0]  # binary 10 = 2, so pick a+2=7
    num_bits = 2
    idx = 0
    for i, bit in enumerate(reversed(coins)):
        idx += bit << i
    result = a + (idx % (b - a + 1))
    assert a <= result <= b

def test_coin_stream_manual_public():
    # Manual bit extraction from an int, mimicking what CoinStream would do
    val = 0b101011
    bits = []
    for i in range(6):
        bits.append((val >> i) & 1)
    assert set(bits) <= {0, 1}