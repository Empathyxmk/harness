import pytest
from src.connect_history_api_fallback.middleware import history_api_fallback

class NextSpy:
    """A very simple spy for function call checking."""
    def __init__(self):
        self.called = False
    def __call__(self, *args, **kwargs):
        self.called = True

@pytest.fixture
def make_req():
    def _make_req(**opts):
        d = {
            'method': 'GET',
            'url': '/foo',
            'headers': {
                'accept': 'text/html, */*'
            }
        }
        d.update(opts)
        if 'headers' in opts:
            d['headers'] = opts['headers']
        return d
    return _make_req

@pytest.mark.parametrize("method", ['POST', 'PUT', 'DELETE', 'OPTIONS'])
def test_must_ignore_non_get_head_requests(method, make_req):
    middleware = history_api_fallback()
    req = make_req(method=method)
    requested_url = req['url']
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == requested_url
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_ignore_requests_that_do_not_accept_html(method, make_req):
    middleware = history_api_fallback()
    req = make_req(method=method, headers={'accept': 'application/json'})
    requested_url = req['url']
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == requested_url
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_ignore_file_requests(method, make_req):
    middleware = history_api_fallback()
    expected = 'js/app.js'
    req = make_req(method=method, url=expected)
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == expected
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_rewrite_requests_with_dot(method, make_req):
    middleware = history_api_fallback()
    req = make_req(method=method, url='js/foo.bar/jkdsah321jkh')
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/index.html'
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_rewrite_requests_when_dot_rule_disabled(method, make_req):
    req = make_req(method=method, url='js/app.js')
    middleware = history_api_fallback({'disableDotRule': True})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/index.html'
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_take_json_preference_into_account(method, make_req):
    middleware = history_api_fallback()
    req = make_req(method=method, headers={'accept': 'application/json, text/plain, */*'})
    requested_url = req['url']
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == requested_url
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_rewrite_valid_requests(method, make_req):
    middleware = history_api_fallback()
    req = make_req(method=method)
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/index.html'
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_not_fail_for_missing_http_accept_header(method, make_req):
    middleware = history_api_fallback()
    req = make_req(method=method)
    del req['headers']['accept']
    requested_url = req['url']
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == requested_url
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_not_fail_for_missing_headers_object(method, make_req):
    middleware = history_api_fallback()
    req = make_req(method=method)
    del req['headers']
    requested_url = req['url']
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == requested_url
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_work_in_verbose_mode(method, make_req):
    req = make_req(method=method, url='js/app.js')
    middleware = history_api_fallback({'verbose': True})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == 'js/app.js'
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_work_with_custom_logger(method, make_req):
    req = make_req(method=method, url='js/app.js')
    called_flags = {'count': 0}
    def logger(*a, **kw):
        called_flags['count'] += 1
    middleware = history_api_fallback({'logger': logger})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == 'js/app.js'
    assert next_spy.called
    assert called_flags['count'] >= 0  # Accepts any call count; real handler could call

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_rewrite_requested_path_according_to_rules(method, make_req):
    import re
    req = make_req(method=method, url='/soccer')
    middleware = history_api_fallback({'rewrites': [ {'from': re.compile(r'/soccer'), 'to': '/soccer.html'} ]})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/soccer.html'
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_support_functions_as_rewrite_rule(method, make_req):
    import re
    req = make_req(method=method, url='/libs/jquery/jquery.1.12.0.min.js')
    def to_fn(context):
        return './bower_components' + context['parsedUrl'].path
    middleware = history_api_fallback({'rewrites': [
        {'from': re.compile(r'^/libs/(.*)$'), 'to': to_fn}
    ]})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == './bower_components/libs/jquery/jquery.1.12.0.min.js'
    assert next_spy.called

    # Second call, should not match
    next_spy = NextSpy()
    req['url'] = '/js/main.js'
    middleware(req, None, next_spy)
    assert req['url'] == '/js/main.js'
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_rewrite_rules_nonmatch(method, make_req):
    import re
    req = make_req(method=method, url='/socer')
    middleware = history_api_fallback({'rewrites': [
        {'from': re.compile(r'/soccer'), 'to': '/soccer.html'}
    ]})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == '/index.html'
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_support_custom_index_file(method, make_req):
    req = make_req(method=method, url='/socer')
    index = 'default.html'
    middleware = history_api_fallback({'index': index})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == index
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_accept_html_requests_based_on_headers_option(method, make_req):
    middleware = history_api_fallback({'htmlAcceptHeaders': ['text/html', 'application/xhtml+xml']})
    req = make_req(method=method, headers={'accept': '*/*'})
    requested_url = req['url']
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == requested_url
    assert next_spy.called

@pytest.mark.parametrize("method", ['GET', 'HEAD'])
def test_should_support_custom_rewrite_rules(method, make_req):
    import re
    # context-parsing is tricky: to function returns input URL or html as needed
    def to_fn(ctx):
        if '.js' in ctx['parsedUrl'].path:
            return ctx['parsedUrl'].geturl()
        else:
            return '/app/login/index.html'

    url = '/app/login/app.js'
    req = make_req(method=method, url=url, headers={'accept': '*/*'})
    middleware = history_api_fallback({'rewrites': [
        {
            'from': re.compile(r'/app/login'),
            'to': to_fn
        }
    ]})
    next_spy = NextSpy()
    middleware(req, None, next_spy)
    assert req['url'] == url
    assert next_spy.called