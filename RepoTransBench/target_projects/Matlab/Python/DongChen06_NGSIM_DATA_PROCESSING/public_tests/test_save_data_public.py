import os
import pytest
import scipy.io
import numpy as np
from src.ngsim_data_processing.save_data import save_data

def test_save_data_public_valid(tmp_path):
    # Different struct and filename
    testStruct = {'a': -42, 'myvec': np.arange(11, 21)}
    output_path = tmp_path / 'public_test_output.mat'
    save_data(str(output_path), testStruct)
    assert output_path.exists()
    loaded = scipy.io.loadmat(str(output_path))
    assert 'a' in loaded and 'myvec' in loaded
    os.remove(str(output_path))

def test_save_data_public_forbidden_characters(tmp_path):
    # Try error: filename with forbidden characters
    testStruct = {'a': -42, 'myvec': np.arange(11, 21)}
    # ':' is invalid on Windows and root directories need permission on Linux; so just check exception
    badname = ':/badfile.mat'
    with pytest.raises(Exception):
        save_data(badname, testStruct)

def test_save_data_public_sparse_matrix(tmp_path):
    from scipy.sparse import csr_matrix
    # Try error: struct containing sparse matrix
    sC = {'sparse': csr_matrix([[1, 0], [0, 1]])}
    filename = tmp_path / 'public_sparse.mat'
    # Savemat supports sparse only with proper MATLAB version -- for portability, expect failure
    with pytest.raises(Exception):
        save_data(str(filename), sC)