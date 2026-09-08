import pytest

class MockExec:
    def __init__(self):
        self.calls = []

    def __call__(self, success, fail, service, action, args):
        self.calls.append((success, fail, service, action, args))

    def reset(self):
        self.calls = []

@pytest.fixture
def mock_exec(monkeypatch):
    exec = MockExec()
    # Simulate mock of import
    monkeypatch.setattr('builtins.mock_exec', exec)
    return exec

class Whitelist:
    def __init__(self, exec_func):
        self._exec = exec_func

    def match(self, url, patterns, callback):
        self._exec(callback, callback, 'WhitelistAPI', 'URLMatchesPatterns', [url, patterns])

    def test(self, url, callback):
        self._exec(callback, callback, 'WhitelistAPI', 'URLIsAllowed', [url])

@pytest.fixture
def whitelist(mock_exec):
    return Whitelist(mock_exec)

def test_match_calls_exec_correct_parameters_basic(whitelist, mock_exec):
    callback = lambda: None
    url = 'http://example.com'
    patterns = ['http://*/*']
    whitelist.match(url, patterns, callback)
    assert mock_exec.calls[-1] == (callback, callback, 'WhitelistAPI', 'URLMatchesPatterns', [url, patterns])

def test_match_calls_exec_even_if_patterns_empty(whitelist, mock_exec):
    callback = lambda: None
    url = 'http://test.com'
    patterns = []
    whitelist.match(url, patterns, callback)
    assert mock_exec.calls[-1] == (callback, callback, 'WhitelistAPI', 'URLMatchesPatterns', [url, patterns])

def test_match_handles_undefined_callback_gracefully(whitelist, mock_exec):
    url = 'http://example.org'
    patterns = ['https://*/*']
    whitelist.match(url, patterns, None)
    assert mock_exec.calls[-1] == (None, None, 'WhitelistAPI', 'URLMatchesPatterns', [url, patterns])

def test_test_calls_exec_correct_parameters_basic(whitelist, mock_exec):
    callback = lambda: None
    url = 'http://allowed.com'
    whitelist.test(url, callback)
    assert mock_exec.calls[-1] == (callback, callback, 'WhitelistAPI', 'URLIsAllowed', [url])

def test_test_calls_exec_when_url_is_undefined(whitelist, mock_exec):
    callback = lambda: None
    url = None
    whitelist.test(url, callback)
    assert mock_exec.calls[-1] == (callback, callback, 'WhitelistAPI', 'URLIsAllowed', [url])

def test_test_handles_undefined_callback_gracefully(whitelist, mock_exec):
    url = 'http://something.com'
    whitelist.test(url, None)
    assert mock_exec.calls[-1] == (None, None, 'WhitelistAPI', 'URLIsAllowed', [url])