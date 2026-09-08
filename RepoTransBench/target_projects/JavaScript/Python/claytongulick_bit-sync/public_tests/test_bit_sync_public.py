import pytest
import numpy as np

from src.bit_sync import BSync

def test_readInt32_public_cases():
    arr = np.array([0x78, 0x56, 0x34, 0x12], dtype='uint8')
    assert BSync.util.readInt32(arr, 0) == 305419896

    arr2 = np.array([0xff, 0xff, 0x00, 0x00], dtype='uint8')
    assert BSync.util.readInt32(arr2, 0) == 65535

    arr3 = np.array([0x00, 0x00, 0x01, 0x00], dtype='uint8')
    assert BSync.util.readInt32(arr3, 0) == 65536

def test_adler32_public():
    arr = np.array([10,20,30], dtype='uint8')
    out = BSync.util.adler32(0, 3, arr)
    assert out.a == 1 + 10 + 20 + 30
    assert out.b == sum([1+10, 1+10+20, 1+10+20+30])
    assert out.checksum == ((out.b << 16) | out.a)

    # Also returns 1 if length == 0, even if buffer nonempty
    assert BSync.util.adler32(0, 0, np.array([1,2,3,4], dtype='uint8')).checksum == 1

def test_makeBlockChecksums_public_cases():
    arr = np.array([8,8,8, 7,7,7, 6], dtype='uint8')
    blocks = BSync.util.makeBlockChecksums(arr, 3)
    assert len(blocks) == 3
    for block in blocks:
        assert isinstance(block['weak'], int)
        assert isinstance(block['strong'], str)

    assert BSync.util.makeBlockChecksums(np.array([], dtype='uint8'), 2) == []

def test_padBuffer_public_variants():
    arr = np.array([10,20], dtype='uint8')
    padded = BSync.util.padBuffer(arr, 4)
    assert len(padded) == 4
    assert padded[0] == 10
    assert padded[1] == 20
    assert padded[3] == 0

    arr2 = np.array([9,8,7], dtype='uint8')
    result = BSync.util.padBuffer(arr2, 3)
    np.testing.assert_array_equal(result, arr2)

    out = BSync.util.padBuffer(np.array([], dtype='uint8'), 0)
    np.testing.assert_array_equal(out, np.array([], dtype='uint8'))

def test_main_api_public_diff_and_patch():
    buf1 = np.array([10,11,12,13,14,15,16,17], dtype='uint8')
    buf2 = np.array([10,99,12,13,55,15,88,17], dtype='uint8')
    block_size = 4
    a_blocks = BSync.util.makeBlockChecksums(buf1, block_size)
    b_blocks = BSync.util.makeBlockChecksums(buf2, block_size)
    diff = BSync.diff(buf1, block_size, b_blocks)
    assert isinstance(diff, list)
    patched = BSync.patch(buf2, diff)
    assert isinstance(patched, type(buf1))
    assert len(patched) == len(buf1)

def test_patch_public_returns_original_if_diff_empty_or_null():
    orig = np.array([4,3,2,1], dtype='uint8')
    np.testing.assert_array_equal(BSync.patch(orig, []), orig)
    np.testing.assert_array_equal(BSync.patch(orig, None), orig)

def test_diff_public_empty_ops_non4_blocksize():
    diff = BSync.diff(np.array([], dtype='uint8'), 8, [])
    assert isinstance(diff, list)
    assert len(diff) == 0

def test_diff_public_single_insert_nontrivial():
    buffer = np.array([42, 69], dtype='uint8')
    for b_blocks in [None, []]:
        diff = BSync.diff(buffer, 2, b_blocks)
        assert len(diff) == 1
        assert diff[0]['type'] == 'insert'
        np.testing.assert_array_equal(diff[0]['data'], buffer)

def test_patch_concat_only_insert_ops_public():
    b1 = np.array([3,4], dtype='uint8')
    b2 = np.array([5,6,7], dtype='uint8')
    diff = [
        {'type': 'insert', 'data': b1},
        {'type': 'insert', 'data': b2}
    ]
    result = BSync.patch(np.array([], dtype='uint8'), diff)
    assert list(result) == [3,4,5,6,7]

def test_patch_returns_original_for_empty_ops_public():
    orig = np.array([123, 124], dtype='uint8')
    np.testing.assert_array_equal(BSync.patch(orig, []), orig)