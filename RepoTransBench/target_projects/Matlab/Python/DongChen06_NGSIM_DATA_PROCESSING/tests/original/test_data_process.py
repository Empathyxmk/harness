import pytest
from src.ngsim_data_processing import data_process

def test_data_process_runs():
    """
    Test that data_process function runs without raising
    """
    data_process.data_process()  # Should not raise