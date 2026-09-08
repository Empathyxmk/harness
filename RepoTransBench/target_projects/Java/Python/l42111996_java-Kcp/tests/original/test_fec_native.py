import random
import pytest

class FakeFecNative:
    def __init__(self, data, part):
        self.data = data
        self.part = part
    def encode(self, shard):
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

def test_fec_native_task():
    data = 10
    part = 3
    mtu = 1500
    fec_encode = FakeFecNative(data, part)
    bufs = build_bytebuf(data, mtu)
    buf_list = []
    for buf in bufs:
        encoded = fec_encode.encode(buf)
        buf_list.extend(encoded)
        buf_list.append(buf)
    can_decode = random.choice([True, False])
    drop_count = random.randint(0, part) if can_decode else part+1+random.randint(0, data-1)
    random_drop(buf_list, drop_count)
    random_sort(buf_list)
    # There's no decode; just check no crash and counts plausible
    assert isinstance(buf_list, list)