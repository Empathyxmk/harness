import cemu.log

def test_register_and_log_public():
    messages = []
    cemu.log.register_sink(messages.append)
    cemu.log.log("test log public message")
    assert messages[-1] == "test log public message"
    cemu.log.unregister_sink(messages.append)
    # Try logging with no sinks should not raise
    cemu.log.log("after unregister")
    assert "test log public message" in messages

def test_error_and_warn_info_ok_dbg_public(monkeypatch):
    msgs = []
    cemu.log.register_sink(msgs.append)
    cemu.log.error("an error occurred")
    assert msgs[-1].startswith("[ERROR]")
    cemu.log.warn("a warning")
    assert msgs[-1].startswith("[WARNING]")
    cemu.log.info("info message")
    assert msgs[-1].startswith("[INFO]")
    cemu.log.ok("operation succeeded")
    assert msgs[-1].startswith("[SUCCESS]")

    monkeypatch.setattr("cemu.const.DEBUG", True)
    cemu.log.dbg("debugging")
    assert msgs[-1].startswith("[DEBUG]")

    cemu.log.unregister_sink(msgs.append)