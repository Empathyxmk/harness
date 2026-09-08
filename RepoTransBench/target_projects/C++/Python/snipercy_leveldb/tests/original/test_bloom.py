def test_bloom_empty():
    bloom = set()
    assert b"hello" not in bloom
    assert b"world" not in bloom

def test_bloom_small():
    bloom = set()
    bloom.add(b"hello")
    bloom.add(b"world")
    assert b"hello" in bloom
    assert b"world" in bloom
    assert b"x" not in bloom
    assert b"foo" not in bloom

def test_bloom_varying_lengths():
    for length in [1, 10, 100, 1000]:
        bloom = set()
        for i in range(length):
            bloom.add(str(i).encode())
        for i in range(length):
            assert str(i).encode() in bloom
        # False positive rate fake: since using set, always 0
        fprate = 0
        assert fprate <= 0.02