import pytest
import numpy as np

from src.lips.load_2dplanedata import load_2dplanedata

def test_load_data_numeric_public(tmp_path):
    temp_file = tmp_path / "tempfile.txt"
    data_sample = np.array([[2, 2, 4, 2], [4, 2, 4, 5], [4, 5, 2, 5]])
    np.savetxt(temp_file, data_sample, fmt='%d')
    result = load_2dplanedata(str(temp_file))
    np.testing.assert_array_equal(result, data_sample)

def test_empty_file_public(tmp_path):
    temp_file = tmp_path / "empty.txt"
    with open(temp_file, "w") as f:
        pass
    result = load_2dplanedata(str(temp_file))
    assert result is None or (hasattr(result, '__len__') and len(result) == 0)