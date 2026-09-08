import os
import pytest
import scipy.io
from src.ngsim_data_processing.save_data import save_data

def test_save_data_basic(tmp_path):
    # Basic valid save test
    dummyStruct = {'x': 5, 'y': list(range(1, 11))}
    output_path = tmp_path / 'test_output.mat'
    save_data(str(output_path), dummyStruct)
    assert output_path.exists()
    data = scipy.io.loadmat(str(output_path))
    # Keys in .mat are always arrays - check presence
    assert 'x' in data and 'y' in data
    os.remove(str(output_path))

def test_save_data_invalid_directory(tmp_path):
    # Try error: invalid filename (directory does not exist)
    dummyStruct = {'x': 5, 'y': list(range(1, 11))}
    bad_dir = tmp_path / 'nonsense_dir'
    filename = str(bad_dir / 'test_output.mat')
    with pytest.raises(FileNotFoundError):
        save_data(filename, dummyStruct)

def test_save_data_function_handle(tmp_path):
    # Try error: invalid variable (e.g., function handle)
    s = {'invalid': lambda x: x+1}
    filename = tmp_path / 'test_output2.mat'
    with pytest.raises(ValueError):
        save_data(str(filename), s)