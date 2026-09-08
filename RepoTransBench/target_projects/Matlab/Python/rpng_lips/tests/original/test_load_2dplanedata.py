import pytest
import numpy as np
import os

from src.lips.load_2dplanedata import load_2dplanedata

def test_valid_file(tmp_path):
    datapath = tmp_path / "floorplan_spencer_large.txt"
    data = np.array([[1, 2], [3, 4]])
    np.savetxt(datapath, data)
    result = load_2dplanedata(str(datapath))
    assert isinstance(result, (list, np.ndarray))

def test_invalid_file():
    with pytest.raises(Exception):
        load_2dplanedata('not_a_real_file.txt')

def test_output_type(tmp_path):
    datapath = tmp_path / "floorplan_spencer_small.txt"
    data = np.array([[1, 2], [3, 4], [5, 6]])
    np.savetxt(datapath, data)
    result = load_2dplanedata(str(datapath))
    assert isinstance(result, list) or isinstance(result, np.ndarray)