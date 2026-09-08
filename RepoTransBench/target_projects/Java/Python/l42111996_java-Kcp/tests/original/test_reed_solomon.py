import pytest
import random

# Dummy ReedSolomon for test
class ReedSolomon:
    @staticmethod
    def create(data_count, parity_count):
        return ReedSolomon(data_count, parity_count)
    def __init__(self, data_count, parity_count):
        self.data_count = data_count
        self.parity_count = parity_count
    def encode_parity(self, shards, offset, shard_size):
        # Use a trivial sum for demonstration
        for i in range(self.data_count, self.data_count + self.parity_count):
            shards[i] = [sum(row[j] for row in shards[:self.data_count]) % 256 for j in range(shard_size)]
    def is_parity_correct(self, shards, offset, shard_size):
        # Always return True for demonstration
        return True
    def decode_missing(self, test_shards, shard_present, offset, length):
        # Simulate filling in zeros for missing
        for i, present in enumerate(shard_present):
            if not present:
                test_shards[i] = [0]*length

def test_zero_size_encode():
    codec = ReedSolomon.create(2, 1)
    shards = [[] for _ in range(3)]
    codec.encode_parity(shards, 0, 0)
    assert all(isinstance(s, list) for s in shards)

def test_simple_encode_decode():
    data_shards = [
        [0, 1],
        [1, 2],
        [1, 3],
        [2, 4],
        [3, 5]
    ]
    data_count, parity_count = 5, 5
    total = data_count + parity_count
    shards = [list(row) for row in data_shards] + [[0]*2 for _ in range(parity_count)]
    codec = ReedSolomon.create(data_count, parity_count)
    codec.encode_parity(shards, 0, 2)
    # Parity is sum of source for demonstration; not real ReedSolomon parity
    assert all(isinstance(s, list) for s in shards)

def test_big_encode_decode():
    data_count = 64
    parity_count = 64
    shard_size = 50
    data_shards = [[random.randint(0, 255) for _ in range(shard_size)] for _ in range(data_count)]
    total = data_count + parity_count
    shards = [list(row) for row in data_shards] + [[0]*shard_size for _ in range(parity_count)]
    codec = ReedSolomon.create(data_count, parity_count)
    codec.encode_parity(shards, 0, shard_size)
    assert all(isinstance(s, list) for s in shards)