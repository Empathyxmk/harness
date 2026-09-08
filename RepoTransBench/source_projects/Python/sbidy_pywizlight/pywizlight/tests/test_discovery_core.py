import pytest
import asyncio
from unittest.mock import MagicMock, patch

import pywizlight.discovery as discovery_mod
from pywizlight.models import BulbRegistry, DiscoveredBulb

class DummyTransport:
    def __init__(self):
        self.sent = []
        self.closed = False
    def sendto(self, data, addr):
        self.sent.append((data, addr))
    def close(self):
        self.closed = True

class DummyLoop:
    def __init__(self):
        self.calls = 0
        self._futures = []
    def call_later(self, t, cb):  # for broadcast_registration
        self.calls += 1
    def create_future(self):
        fut = asyncio.Future()
        self._futures.append(fut)
        return fut

def test_broadcastprotocol_broadcast_registration():
    loop = DummyLoop()
    registry = BulbRegistry()
    bc = discovery_mod.BroadcastProtocol(loop, registry, "127.0.0.1", asyncio.Future())
    # Should not error if self.transport is None
    bc.broadcast_registration()
    # Now with transport
    dummy = DummyTransport()
    bc.transport = dummy
    bc.broadcast_registration()
    assert any(REGISTER_MSG in args[0] for args in dummy.sent)
    assert dummy.sent[0][1][0] == "127.0.0.1"

REGISTER_MSG = b'{"method":"registration"'
def test_broadcastprotocol_datagram_received_good(caplog):
    loop = DummyLoop()
    registry = BulbRegistry()
    future = asyncio.Future()
    proto = discovery_mod.BroadcastProtocol(loop, registry, "127.0.0.1", future)
    valid_json = b'{"result":{"mac":"OOOO"} }'
    proto.datagram_received(valid_json, ("1.1.1.1", 9999))
    bulbs = registry.bulbs()
    assert any(bulb.mac_address == "OOOO" for bulb in bulbs)

def test_broadcastprotocol_datagram_received_bad_json(caplog):
    loop = DummyLoop()
    registry = BulbRegistry()
    proto = discovery_mod.BroadcastProtocol(loop, registry, "127.0.0.1", asyncio.Future())
    with caplog.at_level("ERROR"):
        proto.datagram_received(b"{foo}", ("2.2.2.2", 9999))
    assert "invalid message" in caplog.text

def test_broadcastprotocol_connection_made_triggers_broadcast():
    registry = BulbRegistry()
    loop = DummyLoop()
    proto = discovery_mod.BroadcastProtocol(loop, registry, "127.2.3.4", asyncio.Future())
    dummy = DummyTransport()
    proto.broadcast_registration = MagicMock()
    proto.connection_made(dummy)
    proto.broadcast_registration.assert_called_once()

def test_broadcastprotocol_connection_lost_sets_result():
    registry = BulbRegistry()
    loop = DummyLoop()
    # TEST: The `future` should be done and result set to None after connection_lost(None)
    future = asyncio.Future()
    proto = discovery_mod.BroadcastProtocol(loop, registry, "1.2.3.4", future)
    proto.transport = DummyTransport()
    proto.connection_lost(None)
    assert proto.future.done() and proto.future.result() is None

    # TEST: The `future` should be set with exception if passed an error, and transport should become None
    fut2 = asyncio.Future()
    proto = discovery_mod.BroadcastProtocol(loop, registry, "1.2.3.4", fut2)
    proto.transport = DummyTransport()
    exception = ValueError("fail")
    proto.connection_lost(exception)
    assert proto.transport is None
    with pytest.raises(ValueError):
        fut2.result()

@pytest.mark.asyncio
async def test_find_wizlights_basic(monkeypatch):
    # Test mostly registry and return
    bulbs = [DiscoveredBulb("10.0.0.2", "aaaa")]
    class _Registry:
        def __init__(self): self._b = bulbs
        def bulbs(self): return self._b
    monkeypatch.setattr(discovery_mod, "BulbRegistry", _Registry)

    # The patch below must target the CURRENT RUNNING LOOP's create_datagram_endpoint method,
    # which is bound at runtime. We'll patch 'asyncio.BaseEventLoop.create_datagram_endpoint'
    # for the scope of this test, and restore it after
    class DummyTransportObj:
        def close(self): pass
    class DummyProto:
        pass
    async def dummy_create_datagram_endpoint(self, *a, **k):
        return DummyTransportObj(), DummyProto()

    # Patch at the class level
    old_cde = asyncio.BaseEventLoop.create_datagram_endpoint
    asyncio.BaseEventLoop.create_datagram_endpoint = dummy_create_datagram_endpoint

    # Also patch socket creation, and that the returned BroadcastProtocol is not used (dummy)
    monkeypatch.setattr(discovery_mod, "create_udp_broadcast_socket", lambda port: object())
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    fut.set_result(None)
    monkeypatch.setattr(loop, "create_future", lambda: fut)
    try:
        result = await discovery_mod.find_wizlights(0.01)
    finally:
        asyncio.BaseEventLoop.create_datagram_endpoint = old_cde  # always restore
    assert result and result[0].ip_address == "10.0.0.2"

@pytest.mark.asyncio
async def test_discover_lights(monkeypatch):
    bulbs = [DiscoveredBulb("10.9.8.7", "bbcc")]
    f = asyncio.Future()
    f.set_result(bulbs)
    monkeypatch.setattr(discovery_mod, "find_wizlights", lambda wait_time, broadcast_address=None: f)
    lights = await discovery_mod.discover_lights()
    assert lights and hasattr(lights[0], "ip")