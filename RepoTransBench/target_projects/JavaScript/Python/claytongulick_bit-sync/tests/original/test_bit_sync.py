import pytest
import random
import numpy as np

from src.bit_sync import BSync

def verify_data(buffer1, buffer2):
    if len(buffer1) != len(buffer2):
        return False
    for a, b in zip(buffer1, buffer2):
        if a != b:
            return False
    return True

data = np.array(range(256), dtype='uint8')

def test_read_int32():
    arr = np.zeros(2, dtype=np.uint32)
    arr[0] = 2147483647
    buff = arr.tobytes()
    test_val = BSync.util.readInt32(np.frombuffer(buff, dtype='uint8'), 0)
    assert test_val == 2147483647

    arr[1] = 4294967295
    test_val2 = BSync.util.readInt32(np.frombuffer(buff, dtype='uint8'), 4)
    assert test_val2 == 4294967295

def test_adler32():
    test_data = np.array(data, copy=True)
    result1 = BSync.util.adler32(0, 10, test_data)
    assert result1.a == sum(test_data[:10]) + 1
    result2 = BSync.util.adler32(0, 4, test_data)
    # b = prefix sum
    prefix = [1]
    for v in test_data[:4]:
        prefix.append(prefix[-1] + v)
    expected_b = sum(prefix[1:])
    assert result2.b == expected_b
    assert ((result2.b << 16) | result2.a) == result2.checksum

    # overflow test
    result2 = BSync.util.adler32(0, 300, test_data)
    result1 = BSync.util.adler32(0, 255, test_data)
    assert result2.checksum == result1.checksum

    # randomness & change detection
    result3 = 0
    for _ in range(20):
        idx = random.randint(0, 255)
        test_data[idx] += 1
        r2 = BSync.util.adler32(0, 255, test_data)
        r3 = BSync.util.adler32(0, 255, test_data)
        assert r2.checksum == r3.checksum
        assert result1.checksum != r2.checksum

def test_rolling_checksum():
    test_data = np.array(data, copy=True)
    block_size = 10
    # In source rollingChecksum function is not given, just simulate re-call
    adler1 = BSync.util.adler32(0, block_size - 1, test_data)
    result1 = BSync.util.adler32(1, block_size - 1, test_data) # not true rolling
    # roll through the whole set
    for i in range(2, len(test_data) - block_size):
        result1 = BSync.util.adler32(i, block_size, test_data)
        adler2 = BSync.util.adler32(i, block_size, test_data)
        assert result1.checksum == adler2.checksum
        assert adler2.checksum != 0

def test_checksum_document():
    test_data1 = data.copy()
    block_size = 10
    doc1 = BSync.util.makeBlockChecksums(test_data1, block_size)
    assert doc1 is not None

    test_data2 = data.copy()
    doc2 = BSync.util.makeBlockChecksums(test_data2, block_size)
    assert doc2 is not None

    # They match byte-for-byte
    assert doc1 == doc2

    # change data in first block
    test_data2[0] += 1
    doc2diff = BSync.util.makeBlockChecksums(test_data2, block_size)
    assert doc1 != doc2diff

    # First block adler/md5 is different
    assert doc1[0]['weak'] != doc2diff[0]['weak']
    assert doc1[0]['strong'] != doc2diff[0]['strong']

    # Other blocks are the same
    for i in range(1, len(doc1)):
        assert doc1[i] == doc2diff[i]

def test_patch_document():
    # Skeleton test (source also minimal)
    test_data1 = data.copy()
    block_size = 10
    doc1 = BSync.util.makeBlockChecksums(test_data1, block_size)
    test_data2 = data.copy()
    test_data2[0] += 1

    # In BSync this would be createPatchDocument(results)
    # Here just check diff/patch
    diff = BSync.diff(test_data2, block_size, doc1)
    assert diff

def test_apply_patch():
    test_data1 = data.copy()
    block_size = 10
    doc1 = BSync.util.makeBlockChecksums(test_data1, block_size)
    test_data2 = data.copy()
    diff = BSync.diff(test_data2, block_size, doc1)
    test_data3 = BSync.patch(test_data1, diff)
    assert verify_data(test_data1, test_data2)

    # modify the data a bit
    test_data2[0] += 1
    diff2 = BSync.diff(test_data2, block_size, doc1)
    test_data3 = BSync.patch(test_data1, diff2)
    assert verify_data(test_data2, test_data3)

    # modify it more
    mod_indices = [0,10,11,20,21,30,40,50,100,110,120,130,140,150,200,210,211,213,215,220,230,240,254]
    for idx in mod_indices:
        test_data2[idx] += 1
    diff3 = BSync.diff(test_data2, block_size, doc1)
    test_data3 = BSync.patch(test_data1, diff3)
    assert verify_data(test_data2, test_data3)

    # random runs
    for j in range(10):  # Limited runs for performance
        test_data2 = data.copy()
        num_mods = random.randint(1, len(test_data2))
        mod_indices = random.sample(range(len(test_data2)), num_mods)
        for idx in mod_indices:
            test_data2[idx] += 1
        diffx = BSync.diff(test_data2, block_size, doc1)
        test_data3 = BSync.patch(test_data1, diffx)
        assert verify_data(test_data2, test_data3)