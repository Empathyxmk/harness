import pytest
from unittest import mock
from bs4 import BeautifulSoup

import sys
import types

# -- Fake jQuery-like mock (public variant, different net name, params) --

class FakeJQuery:
    def __init__(self, html=None, node=None):
        self.html_data = html
        self.length = 1
        self.hide_called = False
        self.show_called = False
        self.empty_called = False
        self.remove_called = False
        self.node = node
        self._children = []
        self._msg_html = ''
        if html and 'div class="qtip"' in html:
            self.node = self
        else:
            self.node = node
    def hide(self):
        self.hide_called = True
        return self
    def show(self):
        self.show_called = True
        return self
    def empty(self):
        self.empty_called = True
        return self
    def remove(self):
        self.remove_called = True
        return self
    def html(self, value=None):
        if value is not None:
            self._msg_html = value
        return self._msg_html
    def get(self, _):
        return self
    def __call__(self, *args, **kwargs):
        if args and hasattr(args[0], 'startswith') and args[0].startswith('.msg'):
            return FakeJQuery()
        if args and args[0] == '.qtip':
            fq = FakeJQuery()
            fq.remove_called = self.remove_called
            return fq
        return self

def fake_jquery_factory(soup):
    def fake_jquery(selector, node=None):
        if selector == "#net-spinner":
            return FakeJQuery(node=node)
        elif selector == "#net-error":
            fj = FakeJQuery(node=node)
            fj._msg_html = ''
            return fj
        elif selector == "#net-warning":
            return FakeJQuery(node=node)
        elif selector == "#net-container":
            return FakeJQuery(node=node)
        elif selector == "#net-title":
            return FakeJQuery(node=node)
        elif selector == "#net-svg":
            return FakeJQuery(node=node)
        elif selector == ".qtip":
            fj = FakeJQuery(node=node)
            fj.remove_called = False
            return fj
        elif selector == '.msg':
            fj = FakeJQuery(node=node)
            return fj
        else:
            return FakeJQuery(node=node)
    return fake_jquery

# Simulate lodash
class FakeLodash:
    @staticmethod
    def isUndefined(value):
        return value is None

@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    # Patch fake modules/Renderer/Editor/Notify
    fake_renderer_calls = {}

    class FakeRenderer:
        def __init__(self, net, svg):
            fake_renderer_calls['net'] = net
            self.net = net
            self.svg = svg

    class FakeEditor:
        def __init__(self, cb):
            self.cb = cb

    class FakeNotify:
        onerror = mock.Mock()
        onwarning = mock.Mock()

    import importlib
    sys.modules['netscope.renderer'] = types.SimpleNamespace(Renderer=FakeRenderer)
    sys.modules['netscope.editor'] = types.SimpleNamespace(Editor=FakeEditor)
    sys.modules['netscope.notify'] = types.SimpleNamespace(Notify=FakeNotify)

    monkeypatch.setattr('builtins._', FakeLodash, raising=False)
    yield

@pytest.fixture
def dom_html():
    html = '''
      <html><body>
        <div id="net-container"></div>
        <div id="net-spinner"></div>
        <div id="net-error"><span class="msg"></span></div>
        <div id="net-warning"><span class="msg"></span></div>
        <div id="net-title"></div>
        <svg id="net-svg"></svg>
        <div class="qtip"></div>
      </body></html>
    '''
    return html

@pytest.fixture
def dom(dom_html):
    soup = BeautifulSoup(dom_html, 'html.parser')
    return soup

@pytest.fixture
def fakejquery(dom):
    return fake_jquery_factory(dom)

@pytest.fixture
def fake_net_public():
    return {"name": "public_network_example"}

@pytest.fixture
def Controller(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    return AppController

@pytest.fixture
def patch_notify(monkeypatch):
    class FakeNotify:
        onerror = mock.Mock()
        onwarning = mock.Mock()
    monkeypatch.setattr('builtins.Notify', FakeNotify, raising=False)

def test_constructor_inits_and_handlers_public(monkeypatch, fakejquery, patch_notify):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    assert c.inProgress is False
    assert callable(c.handleError)
    assert callable(c.handleWarning)
    assert hasattr(c, '$spinner')
    assert c.$spinner.length == 1
    assert True

def test_startLoading_triggers_loader_public(monkeypatch, fakejquery, fake_net_public):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.inProgress = False
    c.$spinner.hide_called = False
    c.$netError = fakejquery("#net-error")
    c.$netError.hide_called = False
    c.$spinner.show_called = False

    state = {'loader_called': False}
    def fake_loader(*args):
        state['loader_called'] = True
        if args and callable(args[-1]):
            args[-1](fake_net_public)
    c.startLoading = lambda loader, *a: fake_loader(*a, lambda net=fake_net_public: None)
    c.startLoading(fake_loader, 500, 800)
    assert state['loader_called'] is True

def test_startLoading_exits_early_public(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.inProgress = True
    loader = mock.Mock()
    def fake_loader(*args):
        loader(*args)
    c.startLoading = lambda loader: None
    c.startLoading(fake_loader)
    assert loader.called is False

def test_completeLoading_shows_network_public(monkeypatch, fakejquery, fake_net_public):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.$spinner.hide_called = False
    c.$netBox = fakejquery("#net-container")
    c.$netBox.show_called = False
    c.svg = "#net-svg"
    svg_elem = fakejquery("#net-svg")
    svg_elem.empty_called = False
    c.completeLoading = lambda net: (
        setattr(c.$spinner, 'hide_called', True),
        setattr(c.$netBox, 'show_called', True),
        setattr(svg_elem, 'empty_called', True),
        setattr(fakejquery(".qtip"), 'remove_called', True),
        setattr(c, 'inProgress', False)
    )
    c.completeLoading(fake_net_public)
    assert c.$spinner.hide_called is True
    assert c.$netBox.show_called is True
    assert svg_elem.empty_called is True
    assert c.inProgress is False

def test_makeLoader_wraps_public(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.startLoading = mock.Mock()
    def demo_loader_pub(): pass
    wrapped = c.makeLoader(demo_loader_pub)
    wrapped('a','b','c')
    c.startLoading.assert_called_with(demo_loader_pub, 'a','b','c')

def test_showEditor_loads_script_public(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    if hasattr(sys.modules['builtins'], 'CodeMirror'):
        delattr(sys.modules['builtins'], 'CodeMirror')
    script_loaded = {'called': False}
    def fake_get_script(src, cb):
        script_loaded['called'] = True
        setattr(sys.modules['builtins'], 'CodeMirror', lambda: None)
        cb()
    setattr(sys.modules['builtins'], 'CodeMirror', None)
    setattr(sys.modules['builtins'], '$', fakejquery)
    $.getScript = fake_get_script
    c.showEditor({'load': lambda: None})
    assert script_loaded['called'] is True

def test_showEditor_does_nothing_if_CodeMirror_public(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    setattr(sys.modules['builtins'], 'CodeMirror', lambda: 42)
    $.getScript = mock.Mock()
    c.showEditor({'load': lambda: None})
    $.getScript.assert_not_called()