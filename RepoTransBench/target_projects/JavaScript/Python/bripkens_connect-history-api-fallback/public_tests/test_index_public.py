import re
import pytest
from src.connect_history_api_fallback.middleware import history_api_fallback

class NextSpy:
    def __init__(self):
        self.called = False
    def __call__(self, *args, **kwargs):
        self.called = True

def make_req(**opts):
    incoming = {
        'method': 'GET',
        'headers': {},
        'url': '/foo'
    }
    incoming.update(opts)
    headers = opts.get('headers', None)
    if headers is not None:
        incoming['headers'] = headers
    return incoming

def test_should_not_rewrite_when_accept_prefers_json_and_fallback_to_index_false():
    middleware = history_api_fallback({'fallbackToIndex': False})
    req = make_req(
        method='GET',
        url='/api/v2024/data',
        headers={'accept': 'application/json, text/plain, */*'}
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/api/v2024/data'
    assert next_spy.called

def test_should_rewrite_when_accept_does_not_prefer_json_and_fallback_true():
    middleware = history_api_fallback()
    req = make_req(
        method='GET',
        url='/new-public',
        headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/index.html'
    assert next_spy.called

def test_should_not_rewrite_on_head_when_json_preferred():
    middleware = history_api_fallback({'fallbackToIndex': False})
    req = make_req(
        method='HEAD',
        url='/v3/public/lookup',
        headers={'accept': 'application/json'}
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/v3/public/lookup'
    assert next_spy.called

def test_should_rewrite_on_head_when_accept_does_not_prefer_json():
    middleware = history_api_fallback()
    req = make_req(
        method='HEAD',
        url='/new/other/route',
        headers={'accept': 'text/html'}
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/index.html'
    assert next_spy.called

def test_should_not_rewrite_request_if_url_has_dot_character():
    middleware = history_api_fallback()
    req = make_req(
        url='/static/my.lib.js'
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/static/my.lib.js'
    assert next_spy.called

def test_should_not_rewrite_dotwell_known_resources():
    middleware = history_api_fallback()
    req = make_req(
        url='/.well-known/acme-challenge/something'
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/.well-known/acme-challenge/something'
    assert next_spy.called

def test_custom_rewrite_uses_first_rule():
    middleware = history_api_fallback({
        'dotRule': False,
        'rewrites': [
            {'from': re.compile(r'^/foo-abc$'), 'to': '/alt1/index.html'},
            {'from': re.compile(r'.'), 'to': '/alt2-fallback.html'}
        ]
    })
    req = make_req(
        url='/foo-abc',
        method='GET',
        headers={'accept': 'text/html'}
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/alt1/index.html'
    assert next_spy.called

def test_custom_rewrite_uses_second_rule():
    middleware = history_api_fallback({
        'dotRule': False,
        'rewrites': [
            {'from': re.compile(r'^/foo-abc$'), 'to': '/alt1/index.html'},
            {'from': re.compile(r'.'), 'to': '/alt2-fallback.html'}
        ]
    })
    req = make_req(
        url='/bar-does-not-match',
        method='GET',
        headers={'accept': 'text/html'}
    )
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/alt2-fallback.html'
    assert next_spy.called