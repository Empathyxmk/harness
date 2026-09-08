import pytest
from src.xsens_imu_driver.main import CallbackHandler, XsDataPacket

def test_packet_buffer_operations():
    cb = CallbackHandler(2)
    p1 = XsDataPacket()
    p2 = XsDataPacket()

    assert not cb.packetAvailable()
    cb.onLiveDataAvailable(None, p1)
    assert cb.packetAvailable()
    cb.onLiveDataAvailable(None, p2)
    assert cb.packetAvailable()

    p3 = XsDataPacket()
    cb.onLiveDataAvailable(None, p3)

    count = 0
    while cb.packetAvailable():
        cb.getNextPacket()
        count += 1
    assert count == 2

def test_packet_buffer_edge_cases():
    cb = CallbackHandler(1)
    p = XsDataPacket()
    cb.onLiveDataAvailable(None, p)
    cb.getNextPacket()
    assert not cb.packetAvailable()
    # Do not call getNextPacket() when not available; would raise AssertionError