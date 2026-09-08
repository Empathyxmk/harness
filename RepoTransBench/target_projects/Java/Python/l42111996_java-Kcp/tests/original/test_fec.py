import random
import pytest

class FakeFec:
    # Minimal fake for test demonstration, not a true FEC impl.
    def __init__(self, data, part):
        self.data = data
        self.part = part
    def encode(self, shard):
        # Return a list of dummy parity shards
        return [bytearray(shard)] * self.part

def build_bytebuf(data_shards, mtu):
    bufs = []
    for i in range(data_shards):
        data = bytearray([random.randint(0, 127) for _ in range(mtu)])
        bufs.append(data)
    return bufs

def random_sort(bufs):
    random.shuffle(bufs)

def random_drop(bufs, drop_count):
    for _ in range(drop_count):
        if bufs:
            del bufs[random.randint(0,len(bufs)-1)]

def test_fec_encode_oom():
    data = 10
    part = 3
    fec_encode = FakeFec(data, part)
    bufs = build_bytebuf(data, 1500)
    # Just check encode returns the correct number of parity shards per input
    for buf in bufs:
        result = fec_encode.encode(buf)
        assert len(result) == part

def test_random_sort_and_drop():
    bufs = [bytearray([i]) for i in range(10)]
    orig = bufs[:]
    random_sort(bufs)
    assert set(tuple(b) for b in bufs) == set(tuple(b) for b in orig)
    random_drop(bufs, 3)
    assert len(bufs) == 7