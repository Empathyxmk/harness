import pytest
from src.xsens_imu_driver.main import CallbackHandler, XsDataPacket

def test_larger_buffer_different_sequence():
    cb = CallbackHandler(3)
    p1 = XsDataPacket()
    p2 = XsDataPacket()
    p3 = XsDataPacket()
    p4 = XsDataPacket()

    assert not cb.packetAvailable()
    cb.onLiveDataAvailable(None, p1)
    assert cb.packetAvailable()
    cb.onLiveDataAvailable(None, p2)
    assert cb.packetAvailable()

    cb.onLiveDataAvailable(None, p3)
    cb.onLiveDataAvailable(None, p4)

    count = 0
    while cb.packetAvailable():
        cb.getNextPacket()
        count += 1
    assert count == 3

def test_buffer_recycle_edge_case():
    cb = CallbackHandler(2)
    p1 = XsDataPacket()
    p2 = XsDataPacket()
    cb.onLiveDataAvailable(None, p1)
    assert cb.packetAvailable()
    cb.getNextPacket()
    assert not cb.packetAvailable()
    cb.onLiveDataAvailable(None, p2)
    assert cb.packetAvailable()
    cb.getNextPacket()
    assert not cb.packetAvailable()