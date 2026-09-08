import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import lafan1.extract as extract

def test_extract_func_identity_public():
    # Use a function from extract and verify identity on new simple data
    data = [10, 12, 11, 8]
    identity = lambda x: x
    result = extract.filter_map(identity, data)
    assert result == data

def test_filter_map_applies_function_public():
    result = extract.filter_map(lambda x: x * 2, [5, 0, 2])
    assert result == [10, 0, 4]

def test_split_by_len_multiple_cases_public():
    seqs = [[0,0,0,3], [7,8], [10]]
    out = extract.split_by_len(seqs, 3)
    assert out == [([0, 0, 0], [3]), ([7, 8], []), ([10], [])]

def test_split_by_len_all_shorter_public():
    seqs = [[-1],[0],[1]]
    out = extract.split_by_len(seqs, 3)
    assert out == [([-1],[]), ([0],[]), ([1],[])]

def test_pad_or_trim_public():
    arr = [9]
    desired = 4
    padded = extract.pad_or_trim(arr, desired, pad_value=-1)
    assert padded == [9, -1, -1, -1]
    trimmed = extract.pad_or_trim([7, 1, 3, 8, 6], 2, pad_value=99)
    assert trimmed == [7, 1]

def test_unpad_public():
    arr = [2,3,0,0]
    out = extract.unpad(arr, pad_value=0)
    assert out == [2,3]
    arr2 = [4,4,4,0]
    out2 = extract.unpad(arr2, pad_value=0)
    assert out2 == [4,4,4]

def test_filter_map_empty_data_public():
    f = lambda x: 0
    out = extract.filter_map(f, [])
    assert out == []