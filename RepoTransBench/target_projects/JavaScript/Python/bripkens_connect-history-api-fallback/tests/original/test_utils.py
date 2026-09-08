from src.connect_history_api_fallback.utils import (
    evaluate_rewrite_rule, accepts_html, get_logger
)
import pytest

def test_evaluate_rewrite_rule_str_target():
    urlObj = {'pathname': '/foo'}
    match = ['/foo']
    reqObj = {}
    assert evaluate_rewrite_rule(urlObj, match, '/bar', reqObj) == '/bar'

def test_evaluate_rewrite_rule_fn_target():
    urlObj = {'pathname': '/foo'}
    match = ['/foo']
    reqObj = {}
    def fn(ctx):
        return '/fromFn'
    assert evaluate_rewrite_rule(urlObj, match, fn, reqObj) == '/fromFn'

def test_evaluate_rewrite_rule_bad_type():
    urlObj = {'pathname': '/foo'}
    match = ['/foo']
    reqObj = {}
    with pytest.raises(ValueError) as excinfo:
        evaluate_rewrite_rule(urlObj, match, 123, reqObj)
    assert str(excinfo.value) == 'Rewrite rule can only be of type string or function.'

def test_accepts_html_true_for_defaults():
    assert accepts_html('text/html,application/xhtml+xml', {}) is True
    assert accepts_html('*/*', {}) is True

def test_accepts_html_honor_custom_headers():
    assert accepts_html('application/my-html', {'htmlAcceptHeaders': ['application/my-html']}) is True
    assert accepts_html('something', {'htmlAcceptHeaders': ['foo/bar']}) is False

def test_accepts_html_false_for_not_matched():
    assert accepts_html('application/json', {}) is False

def test_get_logger_return_provided_logger():
    fake = lambda x: None
    assert get_logger({'logger': fake}) == fake

def test_get_logger_returns_function_no_logger_no_verbose():
    assert callable(get_logger({}))
    assert callable(get_logger())

def test_get_logger_returns_function_on_verbose():
    log = get_logger({'verbose': True})
    assert callable(log)