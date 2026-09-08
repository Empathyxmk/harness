import pytest
from src.zapv2 import brk as brk_module

class DummyZAP:
    def __init__(self):
        self.base = 'BASE/'
        self.last_req = None
    def _request(self, url, params=None):
        self.last_req = (url, params)
        # Return values as compatible with six.next(six.itervalues(...))
        return {'value': 'dummy'}

@pytest.fixture
def brk():
    return brk_module.brk(DummyZAP())

def test_is_break_all(brk):
    assert brk.is_break_all == 'dummy'

def test_is_break_request(brk):
    assert brk.is_break_request == 'dummy'

def test_is_break_response(brk):
    assert brk.is_break_response == 'dummy'

def test_http_message(brk):
    assert brk.http_message == 'dummy'

def test_brk_type_state(brk):
    res = brk.brk('http-all', 'true')
    assert res == 'dummy'

def test_brk_with_scope(brk):
    res = brk.brk('http-request', 'false', scope='myscope')
    assert res == 'dummy'

def test_set_http_message_header_only(brk):
    res = brk.set_http_message('header')
    assert res == 'dummy'

def test_set_http_message_header_and_body(brk):
    res = brk.set_http_message('header', 'body')
    assert res == 'dummy'

def test_cont(brk):
    assert brk.cont() == 'dummy'

def test_step(brk):
    assert brk.step() == 'dummy'

def test_drop(brk):
    assert brk.drop() == 'dummy'

def test_add_http_breakpoint(brk):
    res = brk.add_http_breakpoint('string','url','contains',False,False)
    assert res == 'dummy'

def test_remove_http_breakpoint(brk):
    res = brk.remove_http_breakpoint('string','url','contains',False,False)
    assert res == 'dummy'