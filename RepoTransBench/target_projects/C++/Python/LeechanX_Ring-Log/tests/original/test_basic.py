import pytest
from src.rlog import RingLogSingleton, LOG_INIT, LOG_ERROR

def test_basic_logging(monkeypatch):
    # Reset state before test
    RingLogSingleton.instance().clear()

    LOG_INIT("log", "myname", 3)
    for i in range(10):
        LOG_ERROR("my number is %d", i)
    RingLogSingleton.instance().persist()

    # Validate logs
    entries = RingLogSingleton.instance().entries
    assert "init_path(log, myname, 3)" in entries
    for i in range(10):
        msg = "[ERROR] my number is %d" % i
        assert msg in entries
    assert "persist()" in entries