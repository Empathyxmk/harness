import pytest
from src.rlog import RingLogSingleton, DEBUG, INFO, WARN, FATAL

def test_singleton_and_edge_cases():
    RingLogSingleton.instance().clear()
    log1 = RingLogSingleton.instance()
    log2 = RingLogSingleton.instance()
    assert log1 is log2

    # Multiple init_path with different values
    log1.init_path("dir1", "prog1", DEBUG)
    log2.init_path("dir2", "prog2", INFO)
    log1.init_path(None, None, WARN)

    log1.persist()
    log2.persist()

    # try_append across levels
    for l in range(DEBUG, FATAL+1):
        tag = f"LEVEL-{l}"
        log1.try_append(tag, "msg at level %d", l)

    entries = log1.entries

    assert "init_path(dir1, prog1, 0)" in entries
    assert "init_path(dir2, prog2, 1)" in entries
    assert "init_path(None, None, 2)" in entries
    # One persist should suffice in log
    assert entries.count("persist()") >= 1

    for l in range(DEBUG, FATAL+1):
        assert f"[LEVEL-{l}] msg at level {l}" in entries