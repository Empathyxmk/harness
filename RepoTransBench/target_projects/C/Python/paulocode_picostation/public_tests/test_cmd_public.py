# public_tests/test_cmd_public.py

import pytest
from src import cmd

@pytest.fixture(autouse=True)
def reset_cmd_globals_public():
    """Fixture to reset cmd module globals before each test, specifically for public tests."""
    cmd.reset_globals()
    # Public tests sometimes initialize jump_track differently.
    # The original C code sets jump_track = 3 in its reset_globals for public tests.
    cmd.jump_track = 3
    yield # Allow test to run

def test_interrupt_xlat_cmd_autoseq_public():
    """Public Test: interrupt_xlat CMD_AUTOSEQ, use 0xD and different values."""
    cmd.latched = (3 << 20) | (0xD << 16) # CMD_AUTOSEQ and case 0xD
    cmd.track = 10
    cmd.jump_track = 4 # Changed for public test
    cmd.interrupt_xlat(0, 0)
    assert cmd.track == 10 - 4 * 2
    assert cmd.SENS_data[2] == (1 if (cmd.track & 1) else 0)

def test_interrupt_xlat_cmd_soct_public():
    """Public Test: interrupt_xlat CMD_SOCT sets soct and enables pio (again)."""
    cmd.latched = (4 << 20) # CMD_SOCT
    cmd.interrupt_xlat(0, 0)
    assert cmd.soct == 1

def test_interrupt_xlat_cmd_jump_track_public():
    """Public Test: CMD_JUMP_TRACK different value."""
    cmd.latched = (5 << 20) | (0x2F3 << 4) # CMD_JUMP_TRACK
    cmd.interrupt_xlat(0, 0)
    assert cmd.jump_track == 0x2F3

def test_sled_move_directions_public():
    """Public Test: sled_move FORWARD/REVERSE/STOP difference."""
    # Start stopped
    cmd.sled_move_direction = cmd.SLED_MOVE_STOP

    # Forward
    cmd.latched = (2 << 16) # sub = 2
    cmd.sled_move()
    assert cmd.sled_move_direction == cmd.SLED_MOVE_FORWARD

    # Reverse
    cmd.latched = (3 << 16) # sub = 3
    cmd.sled_move()
    assert cmd.sled_move_direction == cmd.SLED_MOVE_REVERSE

    # Stop
    cmd.latched = (0 << 16) # sub = 0
    cmd.sled_move()
    assert cmd.sled_move_direction == cmd.SLED_MOVE_STOP

def test_sled_move_track_increment_decrement_public():
    """Track increment/decrement when stopped (different start)."""
    cmd.sled_move_direction = cmd.SLED_MOVE_STOP # Ensure it's stopped for track changes
    cmd.track = 0 # Start from 0 for clear testing, same as original

    # Increment
    cmd.latched = (8 << 16) # sub = 8
    cmd.sled_move()
    assert cmd.track == 1

    # Decrement
    cmd.latched = (0xC << 16) # sub = 0xC (12)
    cmd.sled_move()
    assert cmd.track == 0

def test_spindle_public():
    """Public Test: spindle sets SENS_data accordingly (different values)."""
    # Set GFS to 1
    cmd.latched = (6 << 16) # sub = 6
    cmd.spindle()
    assert cmd.SENS_data[10] == 1

    # Set GFS to 0 (using 7 as per public C test)
    cmd.latched = (7 << 16) # sub = 7
    cmd.spindle()
    assert cmd.SENS_data[10] == 0