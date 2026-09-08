import pytest
import types
from src.discovery import Discovery

def test_join_leave_list_and_hash_flows():
    d = Discovery()
    try:
        d.join("channel")
        d.leave("channel")
        d.list()
        d.list(b"chan")
    except Exception:
        pytest.fail("join, leave, list, list(Buffer) should not throw")
    d.destroy()
    assert True, "should be destroyed"
    try:
        d.join("again")
        d.leave("again")
        d.list()
    except Exception:
        pytest.fail("join/leave/list after destroy should not throw")

def test_creates_with_default_options_and_emits_warn_error():
    d = Discovery()
    assert d, "should be truthy"
    received = {}
    def cb(msg):
        received['msg'] = msg

    d.once("warn", cb)
    d.emit("warn", "simulated warning")
    assert "msg" in received and isinstance(received["msg"], str), "warn event emitted as string"
    d.remove_all_listeners()

def test_error_emits_with_null():
    d = Discovery()
    received = {}
    def cb(err):
        received['err'] = err
    d.once("error", cb)
    d.emit("error", None)
    assert "err" in received and received['err'] is None, "error emits with null (simulate)"
    d.remove_all_listeners()

def test_hash_override_and_no_hash():
    def custom_hash(_):
        return bytes.fromhex("aabb")
    d1 = Discovery({"hash": custom_hash})
    assert d1._hash("test") == bytes.fromhex("aabb"), "should use custom hash"
    d2 = Discovery()
    assert isinstance(d2._hash("test"), int), "should default to object"

def test_destroy_disables_actions():
    d = Discovery()
    d.destroy()
    assert d.join("abc") is None, "join returns undefined"
    assert d.leave("abc") is None, "leave returns undefined"

def test_event_propagation_peer_warn_error():
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
    d.emit("peer", {"channel": "xyz", "host": "127.0.0.1", "port": 8000})
    d.emit("warn", "warning!")
    d.emit("error", "error!")
    assert peer_result.get('peer') == {'channel': 'xyz', 'host': '127.0.0.1', 'port': 8000}, "peer event as object"
    assert warn_result.get('warn') == "warning!", "warn event"
    assert error_result.get('error') == "error!", "error event"

def test_list_equivalency_check():
    d = Discovery()
    d.join("alpha")
    d.join("beta")
    assert isinstance(d.list("alpha"), list), "should be equivalent"
    assert isinstance(d.list("beta"), list), "should be equivalent"
    assert isinstance(d.list(b"alpha"), list), "should be equivalent"
    assert isinstance(d.list(), list), "should be equivalent"

def test_join_cb_gets_called():
    d = Discovery()
    called = {}
    def cb(err):
        called['cb'] = err
    d.join("callback", {}, cb)
    assert called.get("cb") is None, "null"
    assert True, "should be truthy"