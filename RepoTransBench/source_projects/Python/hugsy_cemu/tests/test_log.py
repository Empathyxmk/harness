import builtins
import pytest

import cemu.log

def test_register_and_unregister_sink():
    # Define a test logger (mock)
    logs = []
    def cb(msg):
        logs.append(msg)
    cemu.log.register_sink(cb)
    
    # After registering, logger is in set
    assert cb in cemu.log.loggers
    
    cemu.log.log("test1")
    assert logs[-1] == "test1"
    cemu.log.error("e")
    assert logs[-1].startswith("[ERROR]")
    cemu.log.warn("w")
    assert "[WARNING]" in logs[-1]
    cemu.log.info("i")
    assert "[INFO]" in logs[-1]
    cemu.log.ok("o")
    assert "[SUCCESS]" in logs[-1]
    # cemu.log.dbg has a branch on DEBUG, see below

    # Remove and check effect
    cemu.log.unregister_sink(cb)
    assert cb not in cemu.log.loggers

def test_dbg_branch(monkeypatch):
    # DEBUG True
    logs = []
    monkeypatch.setattr("cemu.const.DEBUG", True)
    cemu.log.register_sink(logs.append)
    cemu.log.dbg("D1")
    assert "[DEBUG] D1" in logs[-1]
    cemu.log.unregister_sink(logs.append)
    logs.clear()
    # DEBUG False: should not log
    monkeypatch.setattr("cemu.const.DEBUG", False)
    cemu.log.register_sink(logs.append)
    cemu.log.dbg("D2")
    # Should not append anything (i.e., remains empty or unchanged)
    assert logs == []
    cemu.log.unregister_sink(logs.append)

def test_unregister_sink_missing():
    # Removing a non-registered sink raises KeyError
    with pytest.raises(KeyError):
        cemu.log.unregister_sink(lambda x: x)