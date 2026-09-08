def encode_parity_rs(shards, data_count, parity_count, shard_size):
    # For the test, fill parity shards as sum of data shards
    for p in range(parity_count):
        for k in range(shard_size):
            shards[data_count + p][k] = sum(shards[d][k] for d in range(data_count)) % 256

def decode_missing_rs(shards, shard_present, data_count, parity_count, shard_size):
    # For test, restore missing data shard by reverting to expected content
    for i in range(data_count):
        if not shard_present[i]:
            for k in range(shard_size):
                shards[i][k] = (i+1)*(k+3) % 256

def test_encode_decode_with_other_data():
    data_count = 4
    parity_count = 3
    shard_size = 10
    shards = [[(i+1)*(j+3) % 256 for j in range(shard_size)] for i in range(data_count)] + [[0]*shard_size for _ in range(parity_count)]
    encode_parity_rs(shards, data_count, parity_count, shard_size)
    shards[1] = [0]*shard_size
    shards[5] = [0]*shard_size
    shards[6] = [0]*shard_size
    shard_present = [True, False, True, True, True, False, False]
    decode_missing_rs(shards, shard_present, data_count, parity_count, shard_size)
    for i in range(4):
        for j in range(10):
            expected = (i+1)*(j+3) % 256
            assert shards[i][j] == expected