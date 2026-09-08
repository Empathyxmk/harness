# public_tests/test_subq_public.py

import pytest
from src import subq

@pytest.fixture(autouse=True)
def reset_subq_globals_public():
    """Fixture to reset subq module globals before each test, specifically for public tests."""
    subq.reset_globals()
    # Public test for subq uses a different default for num_logical_tracks
    subq.num_logical_tracks = 3
    yield # Allow test to run

@pytest.fixture
def setup_fake_externs():
    """Fixture to set up fake externs for subq module, mimicking C's main function setup."""
    # This simulates the `is_data_track = fake_is_data_arr; logical_track_to_sector = fake_logical_track_to_sector;`
    # from the C public test main.
    subq.is_data_track = [False, False] # fake_is_data_arr
    subq.logical_track_to_sector = [0, 0] # fake_logical_track_to_sector
    yield
    # Reset them back if necessary, though pytest fixtures usually handle state isolation well.

def test_start_subq_public_sector_0_num_logical_tracks_gt_2(setup_fake_externs):
    """Public Test: sector == 0, num_logical_tracks > 2."""
    subq.sector = 0
    subq.num_logical_tracks = 5 # Changed for public test
    subq.start_subq()
    assert subq.hasData == 1

def test_start_subq_public_sector_2_hasData_true(setup_fake_externs):
    """Public Test: sector == 2 -> hasData = true."""
    subq.sector = 2
    subq.start_subq()
    assert subq.hasData == 1

def test_start_subq_public_sector_3_hasData_false(setup_fake_externs):
    """Public Test: sector == 3 -> hasData = false."""
    subq.sector = 3
    subq.start_subq()
    assert subq.hasData == 0

def test_start_subq_public_sector_gt_2_is_data_track_true(setup_fake_externs):
    """Public Test: sector > 2, is_data_track[1] = true --> update."""
    subq.sector = 5 # Changed for public test
    subq.is_data_track[1] = True
    subq.logical_track_to_sector[1] = 123 # Changed for public test
    subq.start_subq()
    assert subq.sector_for_track_update == 123

def test_start_subq_public_sector_gt_2_is_data_track_false(setup_fake_externs):
    """Public Test: sector > 2, is_data_track[1] = false --> no update."""
    subq.sector = 8 # Changed for public test
    subq.is_data_track[1] = False
    subq.logical_track_to_sector[1] = 77 # Changed for public test
    subq.start_subq()
    assert subq.sector_for_track_update == 0

def test_printf_subq_public_smoke(setup_fake_externs):
    """Public Test: printf_subq (smoke test with new data)."""
    data = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    subq.printf_subq(data)