# public_tests/test_utils_public.py

from src import utils

def test_tobcd_public():
    """Public Test: tobcd with different values."""
    assert utils.tobcd(1) == 0x01
    assert utils.tobcd(27) == 0x27
    assert utils.tobcd(53) == 0x53
    assert utils.tobcd(88) == 0x88

def test_reverse_bits_public():
    """Public Test: reverseBits with different numbers."""
    assert utils.reverse_bits(0b01, 2) == 0b10
    assert utils.reverse_bits(0b110, 3) == 0b011
    assert utils.reverse_bits(0xAA, 8) == 0x55

def test_track_to_sector_and_sectors_per_track_public():
    """Public Test: track_to_sector and sectors_per_track, different values."""
    assert utils.track_to_sector(15) == 15
    assert utils.sectors_per_track(7) == 1