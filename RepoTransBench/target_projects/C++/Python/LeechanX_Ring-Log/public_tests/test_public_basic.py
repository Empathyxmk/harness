import pytest
from src.rlog import RingLogSingleton, LOG_INIT, LOG_WARN

def test_public_basic_logging():
    RingLogSingleton.instance().clear()
    LOG_INIT("public_log", "public_prog", 2)
    for i in range(100, 110):
        LOG_WARN("public value is %d", i)
    RingLogSingleton.instance().persist()

    entries = RingLogSingleton.instance().entries
    assert "init_path(public_log, public_prog, 2)" in entries
    for i in range(100, 110):
        msg = "[WARN] public value is %d" % i
        assert msg in entries
    assert "persist()" in entries