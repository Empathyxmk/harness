import pytest
import asyncio
from src.koajs_cors import cors

def create_ctx(method, origin, headers=None):
    if headers is None:
        headers = {}
    _headers = {}
    def get(h):
        if h.lower() == 'origin':
            return origin
        return headers.get(h)
    class Ctx:
        def __init__(self):
            self.method = method
            self.get = get
            self.header = dict({'origin': origin, **headers})
            self.request = type('Request', (), {'header': dict({'origin': origin, **headers}), 'method': method})()
            self.set = lambda k,v: _headers.__setitem__(k, v)
            self.vary = lambda *a, **k: None
            self._headers = _headers
            self.status = None
    return Ctx()

@pytest.mark.asyncio
class TestCORSMiddlewarePublic:
    @pytest.mark.asyncio
    async def test_default_headers_simple_request(self):
        ctx = create_ctx('GET', 'https://publicsite.example')
        middleware = cors()
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == '*'
        assert called['flag']

    @pytest.mark.asyncio
    async def test_set_allow_origin_with_different_options_origin(self):
        ctx = create_ctx('GET', 'https://foo.public.example')
        middleware = cors({'origin': 'https://foo.allowed.com'})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == 'https://foo.allowed.com'
        assert called['flag']

    @pytest.mark.asyncio
    async def test_options_origin_async_function(self):
        async def origin_fn(ctxX):
            orig = ctxX.get('origin')
            return orig.replace('public', 'allowed') if orig else None
        ctx = create_ctx('GET', 'https://async.public.origin')
        middleware = cors({'origin': origin_fn})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == 'https://async.allowed.origin'
        if 'Vary' in ctx._headers:
            assert isinstance(ctx._headers['Vary'], str)
            assert 'Origin' in ctx._headers['Vary']
        assert called['flag']

    @pytest.mark.asyncio
    async def test_skip_options_origin_function_returns_empty_string(self):
        def origin_fn(ctxX):
            if ctxX.get('origin') and 'skipme' in ctxX.get('origin'):
                return ''
            return 'https://other.com'
        ctx = create_ctx('GET', 'https://skipme.public')
        middleware = cors({'origin': origin_fn})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert 'Access-Control-Allow-Origin' not in ctx._headers
        assert called['flag']

    @pytest.mark.asyncio
    async def test_join_new_array_headers(self):
        ctx = create_ctx('GET', 'https://arrayheader.public')
        middleware = cors({'allowMethods': ['POST', 'PUT'], 'allowHeaders': ['X-Custom-Header', 'Content-Type']})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == '*'
        assert called['flag']

    @pytest.mark.asyncio
    async def test_handle_credentials_true_and_star_origin_with_diff_site(self):
        def origin_fn(ctx):
            return ctx.get('origin')
        ctx = create_ctx('GET', 'https://another.public.origin')
        middleware = cors({'origin': origin_fn, 'credentials': True})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == 'https://another.public.origin'
        assert ctx._headers['Access-Control-Allow-Credentials'] == 'true'
        if 'Vary' in ctx._headers:
            assert isinstance(ctx._headers['Vary'], str)
            assert 'Origin' in ctx._headers['Vary']
        assert called['flag']

    @pytest.mark.asyncio
    async def test_handle_credentials_as_function_with_new_origin(self):
        def origin_fn(ctxX):
            return ctxX.get('origin')
        def credentials_fn(ctxX):
            return ctxX.get('origin') == 'https://credentials.public'
        ctx = create_ctx('GET', 'https://credentials.public')
        middleware = cors({'origin': origin_fn, 'credentials': credentials_fn})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == 'https://credentials.public'
        assert ctx._headers['Access-Control-Allow-Credentials'] == 'true'
        assert called['flag']

    @pytest.mark.asyncio
    async def test_handle_exposeHeaders_and_secureContext_new(self):
        ctx = create_ctx('GET', 'https://headers.public')
        middleware = cors({'exposeHeaders': ['X-Public-Header'], 'secureContext': True})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Expose-Headers'] == 'X-Public-Header'
        assert 'Cross-Origin-Resource-Policy' not in ctx._headers
        assert called['flag']

    @pytest.mark.asyncio
    async def test_set_default_headers_if_origin_missing_variant(self):
        ctx = create_ctx('GET', None)
        middleware = cors()
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == '*'
        assert called['flag']

    @pytest.mark.asyncio
    async def test_call_next_and_handle_error_when_keepHeadersOnError_false(self):
        ctx = create_ctx('GET', 'https://errhandl.public')
        middleware = cors()
        class CustomError(Exception): pass
        error = None
        async def next_func():
            raise CustomError('boom2')
        try:
            await middleware(ctx, next_func)
        except Exception as e:
            error = e
        assert error is not None
        assert str(error) == 'boom2'
        assert hasattr(error, 'headers')
        assert error.headers['Access-Control-Allow-Origin'] == '*'

    @pytest.mark.asyncio
    async def test_attach_headers_to_error_when_keepHeadersOnError_true(self):
        ctx = create_ctx('GET', 'https://errkeephead.public')
        def origin_fn(ctx): return ctx.get('origin')
        middleware = cors({'origin': origin_fn, 'keepHeadersOnError': True})
        class CustomError(Exception): pass
        error = None
        async def next_func():
            raise CustomError('publicerror')
        try:
            await middleware(ctx, next_func)
        except Exception as e:
            error = e
        assert error is not None
        assert str(error) == 'publicerror'
        assert hasattr(error, 'headers')
        assert error.headers['Access-Control-Allow-Origin'] == 'https://errkeephead.public'

    @pytest.mark.asyncio
    async def test_preflight_missing_access_control_request_method(self):
        ctx = create_ctx('OPTIONS', 'https://publicpreflight.example')
        def origin_fn(ctx): return ctx.get('origin')
        middleware = cors({'origin': origin_fn})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx.status is None
        assert 'Access-Control-Allow-Origin' not in ctx._headers
        assert 'Access-Control-Allow-Methods' not in ctx._headers
        assert called['flag']

    @pytest.mark.asyncio
    async def test_set_preflight_headers_with_different_values(self):
        ctx = create_ctx('OPTIONS', 'https://preflight.public.com', {
            'Access-Control-Request-Method': 'DELETE',
            'Access-Control-Request-Headers': 'x-preflight-header,content-type',
            'Access-Control-Request-Private-Network': 'true'
        })
        def origin_fn(ctx): return ctx.get('origin')
        middleware = cors({
            'origin': origin_fn,
            'maxAge': 86400,
            'allowMethods': ['DELETE', 'PUT'],
            'allowHeaders': ['X-Preflight-Header', 'Content-Type'],
            'privateNetworkAccess': True
        })
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx.status == 204
        assert ctx._headers['Access-Control-Allow-Origin'] == 'https://preflight.public.com'
        assert ctx._headers['Access-Control-Allow-Methods'] == 'DELETE,PUT'
        assert ctx._headers['Access-Control-Allow-Headers'] == 'X-Preflight-Header,Content-Type'
        assert ctx._headers['Access-Control-Max-Age'] == '86400'
        assert ctx._headers['Access-Control-Allow-Private-Network'] == 'true'
        assert called['flag'] == False