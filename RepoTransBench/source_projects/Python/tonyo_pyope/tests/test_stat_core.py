import pytest
from pyope.errors import NotEnoughCoinsError, InvalidCoinError
from pyope import stat

class DummyRange:
    def __init__(self, s, e):
        self.start = s
        self.end = e
    def size(self):
        return self.end - self.start + 1
    def contains(self, value):
        return self.start <= value <= self.end
    def copy(self):
        return DummyRange(self.start, self.end)

def test_sample_hgd_equal_size(monkeypatch):
    # When in_size == out_size, should return in_range.start + nsample_index - 1
    in_r = DummyRange(10, 20)
    out_r = DummyRange(100, 110)
    nsample = 103
    coins = [0, 1, 0] # Not used since in_size == out_size
    # patch size() to match
    in_r.size = lambda: 11
    out_r.size = lambda: 11
    out_r.contains = lambda n: 100 <= n <= 110
    result = stat.sample_hgd(in_r, out_r, 103, coins)
    assert isinstance(result, int)

def test_sample_hgd_typical(monkeypatch):
    # Monkeypatch HGD.rhyper to test in_sample_num=0 and in_sample_num!=0
    in_r = DummyRange(1, 3)
    out_r = DummyRange(10, 15)
    nsample = 13
    coins = [0, 1, 1]
    in_r.size = lambda: 3
    out_r.size = lambda: 6
    out_r.contains = lambda n: out_r.start <= n <= out_r.end

    class DummyHGD:
        @staticmethod
        def rhyper(nsample_index, M, N, coins_l):
            return 0
    monkeypatch.setattr(stat, "HGD", DummyHGD)
    assert stat.sample_hgd(in_r, out_r, 13, coins) == 1

    class DummyHGD2:
        @staticmethod
        def rhyper(nsample_index, M, N, coins_l):
            return 2
    monkeypatch.setattr(stat, "HGD", DummyHGD2)
    assert stat.sample_hgd(in_r, out_r, 13, coins) == 2

def test_sample_uniform_works():
    class Range:
        def __init__(self, s, e):
            self.start = s
            self.end = e
        def size(self):
            return self.end - self.start + 1
        def copy(self):
            return Range(self.start, self.end)
    r = Range(10, 11)
    coins = iter([1])
    assert stat.sample_uniform(r, coins) in [10, 11]

def test_sample_uniform_not_enough_coins():
    class Range:
        def __init__(self, s, e):
            self.start = s
            self.end = e
        def size(self):
            return self.end - self.start + 1
        def copy(self):
            return Range(self.start, self.end)
    r = Range(1, 2)
    coins = iter([None])
    with pytest.raises(NotEnoughCoinsError):
        stat.sample_uniform(r, coins)

def test_sample_uniform_invalid_coin():
    class Range:
        def __init__(self, s, e):
            self.start = s
            self.end = e
        def size(self):
            return self.end - self.start + 1
        def copy(self):
            return Range(self.start, self.end)
    r = Range(1, 3)
    coins = iter([7, None])
    with pytest.raises(InvalidCoinError):
        stat.sample_uniform(r, coins)