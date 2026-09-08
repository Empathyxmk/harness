# tests/original/test_utils.py

from src import utils

def test_tobcd():
    """Test tobcd function."""
    assert utils.tobcd(0) == 0x00
    assert utils.tobcd(15) == 0x15
    assert utils.tobcd(45) == 0x45
    assert utils.tobcd(99) == 0x99

def test_reverse_bits():
    """Test reverse_bits function."""
    assert utils.reverse_bits(0b10, 2) == 0b01
    assert utils.reverse_bits(0b101, 3) == 0b101
    assert utils.reverse_bits(0xF0, 8) == 0x0F

def test_track_to_sector_and_sectors_per_track():
    """Test track_to_sector and sectors_per_track functions."""
    assert utils.track_to_sector(8) == 8
    assert utils.sectors_per_track(5) == 1