# tests/original/test_cmd.py

import pytest
from src import cmd

@pytest.fixture(autouse=True)
def reset_cmd_globals():
    """Fixture to reset cmd module globals before each test."""
    cmd.reset_globals()
    yield # Allow test to run

def test_interrupt_xlat_cmd_autoseq():
    """Test interrupt_xlat with CMD_AUTOSEQ and case 0xC."""
    cmd.latched = (3 << 20) | (0xC << 16) # CMD_AUTOSEQ and case 0xC
    cmd.track = 2
    cmd.jump_track = 2
    cmd.interrupt_xlat(0, 0)
    assert cmd.track == 2 + 2 * 2
    assert cmd.SENS_data[2] == (1 if (cmd.track & 1) else 0)

def test_interrupt_xlat_cmd_soct():
    """Test interrupt_xlat with CMD_SOCT."""
    cmd.latched = (4 << 20) # CMD_SOCT
    cmd.interrupt_xlat(0, 0)
    assert cmd.soct == 1

def test_interrupt_xlat_cmd_jump_track():
    """Test CMD_JUMP_TRACK extracts value."""
    cmd.latched = (5 << 20) | (0x5A0 << 4) # CMD_JUMP_TRACK
    cmd.interrupt_xlat(0, 0)
    assert cmd.jump_track == 0x5A0

def test_sled_move_directions():
    """Test sled_move FORWARD/REVERSE/STOP."""
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

def test_sled_move_track_increment_decrement():
    """Test track increment/decrement when stopped."""
    cmd.sled_move_direction = cmd.SLED_MOVE_STOP # Ensure it's stopped for track changes

    cmd.track = 0 # Start from 0 for clear testing

    # Increment
    cmd.latched = (8 << 16) # sub = 8
    cmd.sled_move()
    assert cmd.track == 1

    # Decrement
    cmd.latched = (0xC << 16) # sub = 0xC (12)
    cmd.sled_move()
    assert cmd.track == 0

def test_spindle():
    """Test spindle sets SENS_data."""
    # Set GFS to 1
    cmd.latched = (6 << 16) # sub = 6
    cmd.spindle()
    assert cmd.SENS_data[10] == 1

    # Set GFS to 0
    cmd.latched = (5 << 16) # sub = 5
    cmd.spindle()
    assert cmd.SENS_data[10] == 0