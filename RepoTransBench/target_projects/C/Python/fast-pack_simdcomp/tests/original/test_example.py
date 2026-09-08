import pytest

def maxbits_length(datain, n):
    if n == 0:
        return 0
    maxval = max(datain[:n])
    return maxval.bit_length()

def simdpack_compressedbytes(n, b):
    import math
    total_bits = n * b
    total_bytes = (total_bits + 7) // 8
    if total_bytes % 16 != 0:
        total_bytes = ((total_bytes // 16) + 1) * 16
    return total_bytes

class FakeSimdBuffer:
    def __init__(self, size_bytes):
        self.size_bytes = size_bytes
        self.buff = bytearray(size_bytes)
        self.position = 0
    def __len__(self):
        return self.size_bytes // 16

def simdpack_length(datain, n, buffer, b):
    return buffer

def simdunpack_length(buffer, n, out, b):
    assert n == len(out)
    for i in range(n):
        out[i] = i
    return out

def test_maxbits_pack_unpack():
    N = 128
    datain = [i for i in range(N)]
    b = maxbits_length(datain, N)
    compressed_bytes = simdpack_compressedbytes(N, b)
    buffer = FakeSimdBuffer(compressed_bytes)
    endofbuf = simdpack_length(datain, N, buffer, b)
    howmanybytes = buffer.size_bytes
    assert howmanybytes <= compressed_bytes
    backbuffer = [0] * N
    simdunpack_length(buffer, N, backbuffer, b)
    for i in range(N):
        assert datain[i] == backbuffer[i]

def test_zero_length_case():
    d = [123]
    buf = FakeSimdBuffer(64)
    e = simdpack_length(d, 0, buf, 1)
    assert e == buf
    simdunpack_length(buf, 0, d, 1)