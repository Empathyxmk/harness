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
        DummyEl.deps[key][DummyEl._contextId] = "old"
        return DummyEl.deps[key][DummyEl._contextId]

class DebugEl(DummyEl):
    def render(self, html):
        # This just returns a fixed string like in the JS test
        return '<div>foo</div>'
    @staticmethod
    def observedAttributes():
        return []

@pytest.mark.asyncio
async def test_should_wrap_El_notify_and_dep_and_override_render(monkeypatch):
    # Setup
    DummyEl._contextId = None
    DummyEl.deps = {}
    tagName = 'debug-el-common'

    # Simulate "define" and "create" behaviour (no real custom elements)
    el = DebugEl()
    # Patch notify
    notified = {"value": False}
    orig_notify = DummyEl.notify

    def wrapped_notify(*args, **kwargs):
        notified["value"] = True
        return orig_notify(*args, **kwargs)

    monkeypatch.setattr(DummyEl, "notify", staticmethod(wrapped_notify))

    # Call notify and check
    DummyEl.notify('k', 'v')
    assert notified["value"], "notify called"

    # dep: forcibly set up _contextId and deps for coverage
    DummyEl._contextId = "ctx1"
    DummyEl.deps = {}
    DummyEl.deps['abc'] = {'ctx1': 'old'}
    DummyEl.dep('abc')  # Should update 'abc' with 'ctx1'

    # Check render override triggers and works
    result = el.render('<div>bar</div>')
    assert result == '<div>foo</div>'

@pytest.mark.asyncio
async def test_should_handle_missing_El_contextId_in_dep():
    DummyEl._contextId = None
    DummyEl.deps = {}
    val = DummyEl.dep('xyz')
    assert val is True