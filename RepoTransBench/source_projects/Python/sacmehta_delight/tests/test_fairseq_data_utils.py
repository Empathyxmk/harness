import pytest
from fairseq.data import data_utils
import numpy as np

def test_collate_tokens_basic():
    arr = [np.array([1, 2, 3]), np.array([4, 5])]
    res = data_utils.collate_tokens(arr, 0)
    assert res.shape[1] == max(len(a) for a in arr)
    assert (res[:, :len(arr[0])] == arr[0]).all(axis=None) or (res[:, :len(arr[1])] == arr[1]).all(axis=None)

def test_convert_padding_direction():
    arr = np.array([[0,1,2,3,0,0],[0,4,5,0,0,0]])
    pad_idx = 0
    y = data_utils.convert_padding_direction(arr.copy(), pad_idx, right_to_left=True)
    assert (y[0,0] == 0) and (y[0,-1] == 3)
    z = data_utils.convert_padding_direction(arr.copy(), pad_idx, right_to_left=False)
    assert (z == arr).all()

def test_strip_pad():
    arr = np.array([1,2,3,0,0,0])
    result = data_utils.strip_pad(arr, pad=0)
    assert (result == np.array([1,2,3])).all()

def test_move_to_cuda_cpu(monkeypatch):
    # We use monkeypatch to fake torch
    fake = type('torch', (), {"Tensor": lambda x: x, "device": lambda *a,**k: None})
    monkeypatch.setitem(__import__('sys').modules, "torch", fake)
    arr = [1,2]
    assert data_utils.move_to_cuda(arr) == arr
    assert data_utils.move_to_cpu(arr) == arr

def test_dict2namespace():
    d = {"a": 1, "b": 2}
    ns = data_utils.dict2namespace(d)
    assert ns.a == 1 and ns.b == 2