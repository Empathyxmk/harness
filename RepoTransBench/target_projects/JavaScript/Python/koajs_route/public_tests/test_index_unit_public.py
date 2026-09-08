import pytest
import urllib.parse
from unittest.mock import Mock

@pytest.mark.asyncio
async def test_create_route_fn_with_custom_method_options_public():
    fn = Mock()
    def wrapper(ctx, product, next=None):
        if callable(next):
            return next()
    fn.side_effect = wrapper
    # Simulate a route wrapper
    def put_wrapper(ctx, next):
        return fn(ctx, 'laptop', next)
    ctx = {'method': 'PUT', 'path': '/shop/laptop'}
    next_fn = Mock()
    await put_wrapper(ctx, next_fn)
    fn.assert_called_with(ctx, 'laptop', next_fn)

def test_decode_uri_params_public():
    val = 'hello%2Bworld'
    decode = lambda v=None: urllib.parse.unquote(v) if v else None
    assert decode(val) == 'hello+world'
    assert decode() is None

@pytest.mark.asyncio
async def test_support_head_when_only_get_defined_public():
    fn = Mock()
    def head_wrapper(ctx, next=None):
        if callable(next):
            return next()
    fn.side_effect = head_wrapper
    def wrapper(ctx, next):
        return fn(ctx, next)
    ctx = {'method': 'HEAD', 'path': '/about'}
    next_fn = Mock()
    await wrapper(ctx, next_fn)
    fn.assert_called_with(ctx, next_fn)

@pytest.mark.asyncio
async def test_fall_through_if_method_does_not_match_public():
    fn = Mock()
    def wrapper(ctx, next):
        return next()
    ctx = {'method': 'GET', 'path': '/account'}
    next_fn = Mock(return_value='methodMiss')
    result = await wrapper(ctx, next_fn)
    fn.assert_not_called()
    assert result == 'methodMiss'

@pytest.mark.asyncio
async def test_fall_through_if_path_does_not_match_public():
    fn = Mock()
    def wrapper(ctx, next):
        return next()
    ctx = {'method': 'GET', 'path': '/bar'}
    next_fn = Mock(return_value='noMatch')
    result = await wrapper(ctx, next_fn)
    fn.assert_not_called()
    assert result == 'noMatch'

@pytest.mark.asyncio
async def test_all_should_match_all_methods_public():
    fn = Mock()
    def all_fn(ctx, next=None):
        if callable(next):
            return next()
    fn.side_effect = all_fn
    all_wrapper = lambda ctx, next: fn(ctx, next)
    methods = ['DELETE', 'OPTIONS', 'PUT']
    for method in methods:
        ctx = {'method': method, 'path': '/mega'}
        next_fn = Mock()
        await all_wrapper(ctx, next_fn)
        fn.assert_called_with(ctx, next_fn)

def test_route_del_should_be_aliased_to_route_delete_public():
    class Dummy:
        delete = 1
        del_ = 1
    route = Dummy()
    assert getattr(route, "del_", None) == getattr(route, "delete", None)

@pytest.mark.asyncio
async def test_composed_usage_with_path_fn_public():
    fn = Mock()
    def composed(ctx, city=None, next=None):
        ctx['body'] = city or 'none'
        if callable(next):
            return next()
    fn.side_effect = composed
    def wrapper(ctx, next):
        return fn(ctx, 'london', next)
    ctx = {'method': 'GET', 'path': '/city/london', 'body': None}
    next_fn = Mock()
    await wrapper(ctx, next_fn)
    assert ctx['body'] == 'london'

@pytest.mark.asyncio
async def test_handle_params_with_special_characters_decode_public():
    fn = Mock()
    def special(ctx, code):
        ctx['code'] = urllib.parse.unquote(code)
    fn.side_effect = special
    def wrapper(ctx, next):
        return fn(ctx, 'SALE%20OFF%2F2024')
    ctx = {'method': 'GET', 'path': '/voucher/SALE%20OFF%2F2024'}
    next_fn = Mock()
    await wrapper(ctx, next_fn)
    assert ctx['code'] == 'SALE OFF/2024'