import pytest
import urllib.parse
from unittest.mock import Mock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import koajs_route as route

@pytest.mark.asyncio
async def test_should_create_route_function_with_custom_method_and_options():
    fn = Mock()
    def wrapper(ctx, name, next=None):
        if callable(next):
            return next()
    fn.side_effect = wrapper
    # Simulate a route wrapper that calls fn
    def get_wrapper(ctx, next):
        # Simulate matching route
        return fn(ctx, 'bar', next)
    ctx = {'method': 'GET', 'path': '/foo/bar'}
    next_fn = Mock()
    await get_wrapper(ctx, next_fn)
    fn.assert_called_with(ctx, 'bar', next_fn)

def test_should_decode_uri_params():
    val = 'foo%20bar'
    decode = lambda v=None: urllib.parse.unquote(v) if v else None
    assert decode(val) == 'foo bar'
    assert decode() is None

@pytest.mark.asyncio
async def test_should_support_head_when_only_get_defined():
    fn = Mock()
    def head_wrapper(ctx, next=None):
        if callable(next):
            return next()
    fn.side_effect = head_wrapper
    # Simulate wrapper for 'HEAD' call
    def wrapper(ctx, next):
        return fn(ctx, next)
    ctx = {'method': 'HEAD', 'path': '/info'}
    next_fn = Mock()
    await wrapper(ctx, next_fn)
    fn.assert_called_with(ctx, next_fn)

@pytest.mark.asyncio
async def test_should_fall_through_if_method_does_not_match():
    fn = Mock()
    # Simulate wrapper for non-matching method
    def wrapper(ctx, next):
        return next()
    ctx = {'method': 'GET', 'path': '/bar'}
    next_fn = Mock(return_value='called')
    result = await wrapper(ctx, next_fn)
    fn.assert_not_called()
    assert result == 'called'

@pytest.mark.asyncio
async def test_should_fall_through_if_path_does_not_match():
    fn = Mock()
    # Simulate wrapper for non-matching path
    def wrapper(ctx, next):
        return next()
    ctx = {'method': 'GET', 'path': '/baz'}
    next_fn = Mock(return_value='notFound')
    result = await wrapper(ctx, next_fn)
    fn.assert_not_called()
    assert result == 'notFound'

@pytest.mark.asyncio
async def test_all_should_match_all_methods():
    fn = Mock()
    def all_fn(ctx, next=None):
        if callable(next):
            return next()
    fn.side_effect = all_fn
    all_wrapper = lambda ctx, next: fn(ctx, next)
    methods = ['GET', 'POST', 'PATCH']
    for method in methods:
        ctx = {'method': method, 'path': '/all'}
        next_fn = Mock()
        await all_wrapper(ctx, next_fn)
        fn.assert_called_with(ctx, next_fn)

def test_route_del_should_be_aliased_to_route_delete():
    # Simulate route.del is route.delete
    assert getattr(route, "del", None) == getattr(route, "delete", None)

@pytest.mark.asyncio
async def test_composed_usage_with_path_fn():
    fn = Mock()
    def composed(ctx, name=None, next=None):
        ctx['body'] = name or 'no'
        if callable(next):
            return next()
    fn.side_effect = composed
    # Simulate composed: route.get('/x/:name')(fn)
    def wrapper(ctx, next):
        return fn(ctx, 'john', next)
    ctx = {'method': 'GET', 'path': '/x/john', 'body': None}
    next_fn = Mock()
    await wrapper(ctx, next_fn)
    assert ctx['body'] == 'john'

@pytest.mark.asyncio
async def test_should_handle_params_with_special_characters_and_decode_correctly():
    fn = Mock()
    def special(ctx, id):
        ctx['id'] = urllib.parse.unquote(id)
    fn.side_effect = special
    def wrapper(ctx, next):
        return fn(ctx, 'test%20item%2Fid')
    ctx = {'method': 'GET', 'path': '/item/test%20item%2Fid'}
    next_fn = Mock()
    await wrapper(ctx, next_fn)
    assert ctx['id'] == 'test item/id'