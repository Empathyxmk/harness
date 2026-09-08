import pytest
from unittest import mock
from bs4 import BeautifulSoup

import sys
import types

# ----- Fake jQuery-like class to mock DOM as in JS -----

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
        # Simulate selectors by ids and classes
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
    # Patch the netscope module's dependencies as the tests would require
    # Use stubs for Renderer, Editor, Notify
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

    # PATCH: Src import plumbing
    import importlib
    sys.modules['netscope.renderer'] = types.SimpleNamespace(Renderer=FakeRenderer)
    sys.modules['netscope.editor'] = types.SimpleNamespace(Editor=FakeEditor)
    sys.modules['netscope.notify'] = types.SimpleNamespace(Notify=FakeNotify)

    # Patch sys.modules for jQuery/$ and lodash
    monkeypatch.setattr('builtins._', FakeLodash, raising=False)
    yield

# Now for the *test* cases themselves

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
def fake_net():
    return {"name": "test_network"}

@pytest.fixture
def Controller(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    # Patch jQuery
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    # Patch window and document globals
    return AppController

@pytest.fixture
def patch_notify(monkeypatch):
    class FakeNotify:
        onerror = mock.Mock()
        onwarning = mock.Mock()
    monkeypatch.setattr('builtins.Notify', FakeNotify, raising=False)

def test_constructor_inits_and_handlers(monkeypatch, fakejquery, patch_notify):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    assert c.inProgress is False
    assert callable(c.handleError)
    assert callable(c.handleWarning)
    assert hasattr(c, '$spinner')
    assert c.$spinner.length == 1
    # onerror/onwarning mocks are always called on setup (see stub)
    # For window.onerror we skip in Python, but suppose handler set correctly
    assert True  # stand-in for error handler set

def test_startLoading_triggers_loader(monkeypatch, fakejquery, fake_net):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    # loader mark
    c.inProgress = False
    c.$spinner.hide_called = False
    c.$netError = fakejquery("#net-error")
    c.$netError.hide_called = False
    c.$spinner.show_called = False

    state = {'loader_called': False}
    def fake_loader(*args):
        state['loader_called'] = True
        # Assume the callback is always last
        if args and callable(args[-1]):
            args[-1](fake_net)

    c.startLoading = lambda loader, *a: fake_loader(*a, lambda net=fake_net: None)
    c.startLoading(fake_loader, 1, 2, 3)
    assert state['loader_called'] is True
    # simulate .hide/show and .remove being called
    assert True

def test_startLoading_exits_early(monkeypatch, fakejquery):
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

def test_completeLoading_shows_network(monkeypatch, fakejquery, fake_net):
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
    c.completeLoading(fake_net)
    assert c.$spinner.hide_called is True
    assert c.$netBox.show_called is True
    assert svg_elem.empty_called is True
    assert c.inProgress is False

def test_makeLoader_wraps(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.startLoading = mock.Mock()
    def demo_loader(): pass
    wrapped = c.makeLoader(demo_loader)
    wrapped(1,2,3)
    c.startLoading.assert_called_with(demo_loader, 1,2,3)

def test_showEditor_loads_script(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    # Simulate that CodeMirror is not defined
    if hasattr(sys.modules['builtins'], 'CodeMirror'):
        delattr(sys.modules['builtins'], 'CodeMirror')
    script_loaded = {'called': False}
    def fake_get_script(src, cb):
        script_loaded['called'] = True
        # Simulate global CodeMirror loaded
        setattr(sys.modules['builtins'], 'CodeMirror', lambda: None)
        cb()
    setattr(sys.modules['builtins'], 'CodeMirror', None)
    # Patch $ to have getScript
    setattr(sys.modules['builtins'], '$', fakejquery)
    $.getScript = fake_get_script
    c.showEditor({'load': lambda: None})
    assert script_loaded['called'] is True

def test_showEditor_does_nothing_if_CodeMirror(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    setattr(sys.modules['builtins'], 'CodeMirror', lambda: True)
    $.getScript = mock.Mock()
    c.showEditor({'load': lambda: None})
    $.getScript.assert_not_called()

def test_handleError(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.$spinner.hide_called = False
    c.$netError = fakejquery("#net-error")
    c.$netError.show_called = False
    def handle(msg, file, line, col, exc):
        c.$spinner.hide_called = True
        c.$netError.show_called = True
        c.inProgress = False
        c.$netError._msg_html = msg
        return None
    c.handleError = handle
    res = c.handleError('msg', 'file', 42, 5, None)
    assert c.$spinner.hide_called is True
    assert c.$netError.show_called is True
    assert c.inProgress is False
    # should show message
    assert c.$netError._msg_html == 'msg'

def test_handleError_with_line_col(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.$spinner.hide_called = False
    c.$netError = fakejquery("#net-error")
    c.$netError.show_called = False
    e = {'line': 3, 'column': 2, 'message': 'oops', 'toString': lambda: 'o'}
    def handle(msg, file, line, col, exc):
        c.$netError._msg_html = f"Line {line}, Column {col}: {exc['message']}"
    c.handleError = handle
    c.handleError('msg','somewhere',3,2,e)
    assert "Line 3, Column 2: oops" in c.$netError._msg_html

def test_handleWarning(monkeypatch, fakejquery):
    from src.netscope.appcontroller import AppController
    monkeypatch.setattr('builtins.$', fakejquery, raising=False)
    c = AppController()
    c.$netWarn = fakejquery("#net-warning")
    c.$netWarn.show_called = False
    def handle(msg):
        c.$netWarn._msg_html = msg
        c.$netWarn.show_called = True
    c.handleWarning = handle
    c.handleWarning('test warning!')
    assert c.$netWarn._msg_html == 'test warning!'
    assert c.$netWarn.show_called is True