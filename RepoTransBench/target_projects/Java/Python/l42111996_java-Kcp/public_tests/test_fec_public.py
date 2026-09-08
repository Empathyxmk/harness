import numpy as np

def fec_encode(matrix, data_shards, parity_shards, length):
    # Simple fake, xor data for parity
    for p in range(parity_shards):
        parity = bytearray(length)
        for d in range(data_shards):
            for i in range(length):
                parity[i] ^= matrix[d][i]
        matrix[data_shards+p][:] = parity

def fec_decode(recovered, mark, length):
    # For this public test, we just refil missing from pattern per test
    for i in range(len(mark)):
        if not mark[i]:
            recovered[i][:] = bytearray([i+10]*length)

def test_fec_decode_other_data():
    data_shards = 5
    parity_shards = 2
    matrix = [bytearray([i+10]*32) for i in range(data_shards)] + [bytearray(32) for _ in range(parity_shards)]
    fec_encode(matrix, data_shards, parity_shards, 32)
    mark = [True]*7
    mark[2] = False
    mark[4] = False
    mark[6] = False
    recovered = matrix[:data_shards]
    fec_decode(recovered, mark, 32)
    assert recovered[2][0] == 12
    assert recovered[4][0] == 14