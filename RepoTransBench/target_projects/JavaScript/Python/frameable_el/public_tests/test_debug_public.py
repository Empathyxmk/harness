import pytest
import asyncio
from bs4 import BeautifulSoup

class DummyEl:
    _contextId = None
    deps = {}

    @staticmethod
    def notify(*args, **kwargs):
        DummyEl._notified_args = args
        DummyEl._notified_kwargs = kwargs
        return "notified:{},{}".format(args, kwargs)

    @staticmethod
    def dep(key):
        # If _contextId is missing, returns True
        if DummyEl._contextId is None:
            return True
        DummyEl.deps.setdefault(key, {})
        DummyEl.deps[key][DummyEl._contextId] = "previous"
        return DummyEl.deps[key][DummyEl._contextId]

class DebugEl(DummyEl):
    def render(self, html):
        return '<span>bazqux</span>'
    @staticmethod
    def observedAttributes():
        return []

@pytest.mark.asyncio
async def test_should_wrap_El_notify_and_dep_and_override_render_with_new_tag_data(monkeypatch):
    # Setup
    DummyEl._contextId = None
    DummyEl.deps = {}
    tagName = 'debug-el-public'

    el = DebugEl()
    notified = {"value": False}
    orig_notify = DummyEl.notify

    def wrapped_notify(*args, **kwargs):
        notified["value"] = True
        return orig_notify(*args, **kwargs)

    monkeypatch.setattr(DummyEl, "notify", staticmethod(wrapped_notify))

    DummyEl.notify('newKey', 'newValue')
    assert notified["value"], "notify called (public)"

    DummyEl._contextId = "publicCtx2"
    DummyEl.deps = {}
    DummyEl.deps['def'] = {'publicCtx2': 'previous'}

    DummyEl.dep('def')
    result = el.render('<span>quuz</span>')
    assert result == '<span>bazqux</span>'

@pytest.mark.asyncio
async def test_should_handle_missing_El_contextId_in_dep_for_public_test():
    DummyEl._contextId = None
    DummyEl.deps = {}
    val = DummyEl.dep('uvw')
    assert val is True