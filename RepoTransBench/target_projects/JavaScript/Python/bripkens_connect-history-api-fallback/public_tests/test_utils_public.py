import pytest
from src.connect_history_api_fallback.utils import evaluate_rewrite_rule, accepts_html, get_logger

def test_evaluate_rewrite_rule_public_string():
    urlObj = {'pathname': '/bar'}
    match = ['/bar']
    reqObj = {}
    assert evaluate_rewrite_rule(urlObj, match, '/baz', reqObj) == '/baz'

def test_evaluate_rewrite_rule_public_function():
    urlObj = {'pathname': '/bar'}
    match = ['/bar']
    reqObj = {}
    called = {}
    def fn(ctx):
        called['val'] = ctx
        return '/fromFnPublic'
    result = evaluate_rewrite_rule(urlObj, match, fn, reqObj)
    assert result == '/fromFnPublic'
    assert called['val'] == {'parsedUrl': urlObj, 'match': match, 'request': reqObj}

def test_evaluate_rewrite_rule_bad_type_public():
    urlObj = {'pathname': '/bar'}
    match = ['/bar']
    reqObj = {}
    with pytest.raises(ValueError) as excinfo:
        evaluate_rewrite_rule(urlObj, match, {}, reqObj)
    assert str(excinfo.value) == 'Rewrite rule can only be of type string or function.'

def test_accepts_html_should_return_true_for_custom():
    assert accepts_html('application/xhtml+xml,application/html', {'htmlAcceptHeaders': ['application/html']})
    assert accepts_html('application/*', {'htmlAcceptHeaders': ['application/*']})

def test_accepts_html_honor_custom_headers_public():
    assert accepts_html('text/x-html', {'htmlAcceptHeaders': ['text/x-html']})
    assert not accepts_html('some-val', {'htmlAcceptHeaders': ['some-header']})

def test_accepts_html_return_false_if_not_matched_public():
    assert not accepts_html('image/svg+xml', {})

def test_get_logger_return_provided_logger_public():
    fake = lambda *a, **kw: 123
    assert get_logger({'logger': fake}) == fake

def test_get_logger_return_function_no_logger_no_verbose_public():
    assert callable(get_logger({}))
    assert callable(get_logger())

def test_get_logger_return_bound_console_log_on_verbose_public():
    log = get_logger({'verbose': True})
    assert callable(log)