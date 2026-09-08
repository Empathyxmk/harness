import pytest
from src.rlog import RingLogSingleton, DEBUG, INFO, WARN, ERROR, FATAL

def test_public_advanced():
    RingLogSingleton.instance().clear()
    logA = RingLogSingleton.instance()
    logB = RingLogSingleton.instance()
    assert logA is logB

    # Use different paths, program names, and log levels
    logA.init_path("pubdirA", "pubprogA", WARN)
    logB.init_path("pubdirB", "pubprogB", ERROR)
    logA.init_path("", "", FATAL)

    logA.persist()
    logB.persist()

    for l in range(FATAL, DEBUG-1, -1):
        tag = f"PUB-LEVEL-{l}"
        logA.try_append(tag, "msg at public level %d", l)

    entries = logA.entries
    assert "init_path(pubdirA, pubprogA, 2)" in entries
    assert "init_path(pubdirB, pubprogB, 3)" in entries
    assert "init_path(, , 4)" in entries

    assert entries.count("persist()") >= 1

    for l in range(FATAL, DEBUG-1, -1):
        assert f"[PUB-LEVEL-{l}] msg at public level {l}" in entries