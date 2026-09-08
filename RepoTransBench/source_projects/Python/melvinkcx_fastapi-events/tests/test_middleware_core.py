import asyncio
import pytest
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_events.handlers.base import BaseEventHandler
from fastapi_events import handler_store
from contextlib import contextmanager

class DummyHandler(BaseEventHandler):
    async def handle_many(self, events):
        # For test: Just store events to a list attribute.
        self.handled = list(events)

@pytest.mark.asyncio
async def test_event_handler_asgi_middleware_http_scope(monkeypatch):
    called = {"app": False, "handled": False}

    async def mock_app(scope, receive, send):
        called["app"] = True
        # Simulate event being stored (event_store)
        from fastapi_events import event_store
        queue = event_store.get()
        queue.append(("fruit", {"apple": 1}))
        # events should be processed after app finishes

    handler = DummyHandler()
    mw = EventHandlerASGIMiddleware(app=mock_app, handlers=[handler])
    # Prepare event_store context so queue works in this thread

    events_handled = []

    async def fake_gather(*tasks):
        # Simulate running handle_many
        await tasks[0]
        events_handled.append(getattr(handler, "handled", []))

    monkeypatch.setattr("asyncio.gather", fake_gather)

    async def send(msg): return None
    async def receive(): return {}

    scope = {"type": "http"}
    await mw(scope, receive, send)
    assert called["app"] is True
    assert isinstance(handler.handled, list)
    assert ("fruit", {"apple": 1}) in handler.handled
    assert events_handled

@pytest.mark.asyncio
async def test_event_handler_asgi_middleware_non_http():
    # Should just call app and _process_events is not invoked
    results = {"app": False}

    async def mock_app(scope, receive, send):
        results["app"] = True

    handler = DummyHandler()
    mw = EventHandlerASGIMiddleware(app=mock_app, handlers=[handler])
    scope = {"type": "lifespan"}
    async def send(msg): pass
    async def receive(): return {}
    await mw(scope, receive, send)
    assert results["app"]

def test_register_and_deregister_handlers():
    handler = DummyHandler()
    mw = EventHandlerASGIMiddleware(
        app=lambda s,r,sn: None, handlers=[handler], middleware_id=2222
    )
    assert 2222 in handler_store
    mw.deregister_handlers()
    assert 2222 not in handler_store
    # deregister_handlers should not error if called again, but raises KeyError
    with pytest.raises(KeyError):
        mw.deregister_handlers()

def test_event_store_ctx_and_res_req_cycle_ctx_debug(monkeypatch):
    handler = DummyHandler()
    mw = EventHandlerASGIMiddleware(app=lambda s,r,sn: None, handlers=[handler])
    logs = []
    monkeypatch.setattr("fastapi_events.middleware.logger.debug", lambda msg: logs.append(msg))
    # Enter event_store_ctx, should log
    with mw.event_store_ctx():
        assert logs and "Setting event_store ctx" in logs[0]
    # After context, logs should show reset
    assert any("Resetting" in m for m in logs)

    with mw.res_req_cycle_ctx():
        pass
    # no exceptions/exiting

def test_del_deregisters(monkeypatch):
    class Dummy(EventHandlerASGIMiddleware):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            # Override id to match
            self._id = id(self)
            self.deregistered = False
        def deregister_handlers(self):
            self.deregistered = True
    dummy = Dummy(app=lambda s,r,sn: None, handlers=[])
    dummy_id = id(dummy)
    # Forcibly call __del__
    dummy.__del__()
    assert dummy.deregistered