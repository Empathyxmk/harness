import pytest
import numpy as np
from src.bit_sync import BSync

def test_main_api_diff_and_patch():
    buf1 = np.array([0,1,2,3,4,5,6,7,8,9], dtype='uint8')
    buf2 = np.array([0,1,9,3,4,50,6,7,8,9], dtype='uint8')
    block_size = 5
    a_blocks = BSync.util.makeBlockChecksums(buf1, block_size)
    b_blocks = BSync.util.makeBlockChecksums(buf2, block_size)
    diff = BSync.diff(buf1, block_size, b_blocks)
    assert isinstance(diff, list)
    patched = BSync.patch(buf2, diff)
    assert isinstance(patched, type(buf1))
    assert len(patched) == len(buf1)

def test_patch_returns_original_if_diff_empty_or_null():
    orig = np.array([1,2,3], dtype='uint8')
    assert (BSync.patch(orig, []) == orig).all()
    assert (BSync.patch(orig, None) == orig).all()

def test_diff_empty_ops_when_buffer_empty():
    diff = BSync.diff(np.array([], dtype='uint8'), 4, [])
    assert isinstance(diff, list)
    assert len(diff) == 0

def test_diff_single_insert_when_b_blocks_null_or_empty():
    buffer = np.array([1,2,3], dtype='uint8')
    for b_blocks in [None, [], None]:
        diff = BSync.diff(buffer, 4, b_blocks)
        assert len(diff) == 1
        assert diff[0]['type'] == 'insert'
        assert np.array_equal(diff[0]['data'], buffer)

def test_patch_concatenates_insert_ops():
    b1 = np.array([5,6], dtype='uint8')
    b2 = np.array([7], dtype='uint8')
    diff = [
        {'type': 'insert', 'data': b1},
        {'type': 'insert', 'data': b2}
    ]
    result = BSync.patch(np.array([], dtype='uint8'), diff)
    assert list(result) == [5,6,7]

def test_patch_returns_original_for_empty_ops():
    orig = np.array([9], dtype='uint8')
    assert (BSync.patch(orig, []) == orig).all()