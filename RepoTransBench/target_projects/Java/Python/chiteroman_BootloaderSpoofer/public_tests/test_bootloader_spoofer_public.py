import pytest
from src.bootloader_spoofer.bootloader_spoofer import BootloaderSpoofer

def test_toggle_spoof_state():
    bs = BootloaderSpoofer()
    # Sequence: spoof, reset, spoof
    bs.spoof()
    assert bs.is_spoofed()
    assert bs.status() == "Spoofed"
    bs.reset()
    assert not bs.is_spoofed()
    assert bs.status() == "Not spoofed"
    bs.spoof()
    assert bs.is_spoofed()
    assert bs.status() == "Spoofed"

def test_multiple_reset():
    bs = BootloaderSpoofer()
    # Try resetting before spoofing, then after spoofing
    bs.reset()  # should remain Not spoofed
    assert not bs.is_spoofed()
    assert bs.status() == "Not spoofed"
    bs.spoof()
    assert bs.is_spoofed()
    bs.reset()
    bs.reset()  # should stay Not spoofed after two resets
    assert not bs.is_spoofed()
    assert bs.status() == "Not spoofed"

def test_alternating_spoof_and_reset():
    bs = BootloaderSpoofer()
    # Spoof -> Reset -> Spoof -> Reset
    bs.spoof()
    assert bs.is_spoofed()
    bs.reset()
    assert not bs.is_spoofed()
    bs.spoof()
    assert bs.is_spoofed()
    bs.reset()
    assert not bs.is_spoofed()
    assert bs.status() == "Not spoofed"

def test_repeated_reset_without_spoof():
    bs = BootloaderSpoofer()
    bs.reset()
    bs.reset()
    # Never spoofed
    assert not bs.is_spoofed()
    assert bs.status() == "Not spoofed"
    # Now spoof and test again
    bs.spoof()
    assert bs.is_spoofed()
    bs.reset()
    assert not bs.is_spoofed()