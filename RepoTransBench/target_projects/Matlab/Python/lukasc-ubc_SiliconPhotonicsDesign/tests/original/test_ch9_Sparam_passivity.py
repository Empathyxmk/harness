import pytest
import os

def VectorFitting_Sparam():
    # Simulate the effect of trying to load a file that doesn't exist.
    raise FileNotFoundError("Could not read file.")

def test_missing_mat_file_error():
    with pytest.raises(FileNotFoundError):
        VectorFitting_Sparam()