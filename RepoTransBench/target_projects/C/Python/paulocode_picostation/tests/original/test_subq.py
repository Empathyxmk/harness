# tests/original/test_subq.py

import pytest
from src import subq

@pytest.fixture(autouse=True)
def reset_subq_globals():
    """Fixture to reset subq module globals before each test."""
    subq.reset_globals()
    yield # Allow test to run

def test_start_subq_sector_0_num_logical_tracks_gt_1():
    """Test: sector == 0, num_logical_tracks > 1 --> hasData = true."""
    subq.sector = 0
    subq.num_logical_tracks = 2
    subq.start_subq()
    assert subq.hasData == 1

def test_start_subq_sector_1_hasData_false():
    """Test: sector == 1 -> hasData = false."""
    subq.sector = 1
    subq.start_subq()
    assert subq.hasData == 0

def test_start_subq_sector_2_hasData_true():
    """Test: sector == 2 -> hasData = true."""
    subq.sector = 2
    subq.start_subq()
    assert subq.hasData == 1

def test_start_subq_sector_gt_2_is_data_track_true():
    """Test: sector > 2, is_data_track[1] = true --> update."""
    subq.sector = 3
    subq.is_data_track[1] = True # C uses 1 for true
    subq.logical_track_to_sector[1] = 199
    subq.start_subq()
    assert subq.sector_for_track_update == 199

def test_start_subq_sector_gt_2_is_data_track_false():
    """Test: sector > 2, is_data_track[1] = false --> no update."""
    subq.sector = 4
    subq.is_data_track[1] = False # C uses 0 for false
    subq.logical_track_to_sector[1] = 202
    subq.start_subq()
    assert subq.sector_for_track_update == 0

def test_printf_subq_smoke():
    """Smoke test for printf_subq."""
    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # This test primarily checks if the function can be called without error.
    # The output is printed to stdout, which pytest captures.
    subq.printf_subq(data)
    # No assert for output, as it's a smoke test for printing