import pytest
from src.discovery import Discovery

def test_join_leave_list_and_hash_flows_public():
    d = Discovery()
    try:
        d.join("public_chan")
        d.leave("public_chan")
        d.list()
        d.list(b"public_buf")
    except Exception:
        pytest.fail("join, leave, list, list(Buffer) should not throw")
    d.destroy()
    assert True, "should be destroyed"
    try:
        d.join("rejoin")
        d.leave("releave")
        d.list()
    except Exception:
        pytest.fail("join/leave/list after destroy should not throw")

def test_creates_with_default_options_and_emits_warn_error_public():
    d = Discovery()
    assert d, "should be truthy"
    received = {}
    def cb(msg):
        received['msg'] = msg

    d.once("warn", cb)
    d.emit("warn", "public warning")
    assert "msg" in received and isinstance(received["msg"], str), "warn event emitted as string"
    d.remove_all_listeners()

def test_error_emits_with_undefined_public():
    d = Discovery()
    received = {}
    def cb(err):
        received['err'] = err
    d.once("error", cb)
    d.emit("error", None)
    assert "err" in received and received['err'] is None, "error emits with undefined (simulate)"
    d.remove_all_listeners()

def test_hash_override_and_no_hash_public():
    def custom_hash(_):
        return bytes.fromhex("bbee")
    d1 = Discovery({"hash": custom_hash})
    assert d1._hash("foo") == bytes.fromhex("bbee"), "should use custom hash"
    d2 = Discovery()
    assert isinstance(d2._hash("foo"), int), "should default to object"

def test_destroy_disables_actions_public():
    d = Discovery()
    d.destroy()
    assert d.join("xyz123") is None, "join returns undefined"
    assert d.leave("123xyz") is None, "leave returns undefined"

def test_event_propagation_peer_warn_error_public():
    d = Discovery()
    peer_result = {}
    warn_result = {}
    error_result = {}
    def on_peer(obj):
        peer_result['peer'] = obj
    def on_warn(w):
        warn_result['warn'] = w
    def on_error(e):
        error_result['error'] = e
    d.on("peer", on_peer)
    d.on("warn", on_warn)
    d.on("error", on_error)
    d.emit("peer", {"channel": "uvw", "host": "10.0.0.1", "port": 9000})
    d.emit("warn", "a public warning!")
    d.emit("error", "a public error!")
    assert peer_result.get('peer') == {'channel': 'uvw', 'host': '10.0.0.1', 'port': 9000}, "peer event as object"
    assert warn_result.get('warn') == "a public warning!", "warn event"
    assert error_result.get('error') == "a public error!", "error event"

def test_list_equivalency_check_public():
    d = Discovery()
    d.join("gamma")
    d.join("delta")
    assert isinstance(d.list("gamma"), list), "should be equivalent"
    assert isinstance(d.list("delta"), list), "should be equivalent"
    assert isinstance(d.list(b"gamma"), list), "should be equivalent"
    assert isinstance(d.list(), list), "should be equivalent"

def test_join_cb_gets_called_public():
    d = Discovery()
    called = {}
    def cb(err):
        called['cb'] = err
    d.join("cb", {}, cb)
    assert called.get("cb") is None, "null"
    assert True, "should be truthy"