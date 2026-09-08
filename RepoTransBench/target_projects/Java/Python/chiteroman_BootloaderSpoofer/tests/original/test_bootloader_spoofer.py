import pytest
from src.bootloader_spoofer.bootloader_spoofer import BootloaderSpoofer

def test_initial_status():
    bs = BootloaderSpoofer()
    assert not bs.is_spoofed()
    assert bs.status() == "Not spoofed"

def test_spoof_sets_spoofed():
    bs = BootloaderSpoofer()
    bs.spoof()
    assert bs.is_spoofed()
    assert bs.status() == "Spoofed"

def test_reset():
    bs = BootloaderSpoofer()
    bs.spoof()
    bs.reset()
    assert not bs.is_spoofed()
    assert bs.status() == "Not spoofed"

def test_multiple_spoof():
    bs = BootloaderSpoofer()
    bs.spoof()
    bs.spoof()  # should not change state or throw
    assert bs.is_spoofed()