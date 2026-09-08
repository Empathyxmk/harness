import pytest
import asyncio
from src.koajs_cors import cors

def mock_ctx(headers=None, method='GET'):
    if headers is None:
        headers = {}
    _headers = {}
    class MockCtx:
        def __init__(self):
            self.method = method
            self.headers = headers
            self._headers = _headers
        def set(self, key, value):
            self._headers[key] = value
        def get(self, key):
            return self.headers.get(key) or self.headers.get(key.lower())
        def vary(self, value):
            self._headers['Vary'] = value
    return MockCtx()

@pytest.mark.asyncio
class TestCORSMiddleware:
    @pytest.mark.asyncio
    async def test_default_headers_simple_requests(self):
        middleware = cors()
        ctx = mock_ctx({'Origin': 'http://example.com'})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == '*'
        assert ctx._headers['Vary'] == 'Origin'
        assert called['flag']

    @pytest.mark.asyncio
    async def test_allow_origin_from_options_origin_string(self):
        middleware = cors({'origin': 'http://site.com'})
        ctx = mock_ctx({'Origin': 'http://example.com'})
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == 'http://site.com'

    @pytest.mark.asyncio
    async def test_options_origin_as_function(self):
        call_data = {}
        async def fn(ctx):
            call_data['called'] = True
            return 'http://abc.com'
        middleware = cors({'origin': fn})
        ctx = mock_ctx({'Origin': 'http://other.com'})
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert call_data.get('called')
        assert ctx._headers['Access-Control-Allow-Origin'] == 'http://abc.com'

    @pytest.mark.asyncio
    async def test_skip_if_options_origin_function_returns_falsy(self):
        call_data = {}
        async def fn(ctx):
            call_data['called'] = True
            return ''
        middleware = cors({'origin': fn})
        ctx = mock_ctx({'Origin': 'http://other.com'})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert call_data.get('called')
        assert 'Access-Control-Allow-Origin' not in ctx._headers
        assert called['flag']

    @pytest.mark.asyncio
    async def test_join_array_headers(self):
        middleware = cors({
            'exposeHeaders': ['A', 'B'],
            'allowMethods': ['GET', 'POST'],
            'allowHeaders': ['X', 'Y']
        })
        ctx = mock_ctx({'Origin': 'x'})
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Expose-Headers'] == 'A,B'

    @pytest.mark.asyncio
    async def test_handle_credentials_true_and_star_origin(self):
        middleware = cors({'credentials': True})
        ctx = mock_ctx({'Origin': 'http://custom.com'})
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Credentials'] == 'true'
        assert ctx._headers['Access-Control-Allow-Origin'] == 'http://custom.com'

    @pytest.mark.asyncio
    async def test_handle_credentials_as_function(self):
        call_data = {}
        async def fn(ctx):
            call_data['called'] = True
            return True
        middleware = cors({'origin': '*', 'credentials': fn})
        ctx = mock_ctx({'Origin': 'http://zzz'})
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert call_data.get('called')
        assert ctx._headers['Access-Control-Allow-Origin'] == 'http://zzz'
        assert ctx._headers['Access-Control-Allow-Credentials'] == 'true'

    @pytest.mark.asyncio
    async def test_handle_exposeHeaders_and_secureContext(self):
        middleware = cors({'exposeHeaders': 'X-Token', 'secureContext': True})
        ctx = mock_ctx({'Origin': 'http://abc'})
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Expose-Headers'] == 'X-Token'
        assert ctx._headers['Cross-Origin-Opener-Policy'] == 'same-origin'
        assert ctx._headers['Cross-Origin-Embedder-Policy'] == 'require-corp'

    @pytest.mark.asyncio
    async def test_set_default_headers_if_origin_missing(self):
        middleware = cors()
        ctx = mock_ctx({})
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == '*'
        assert called['flag']

    @pytest.mark.asyncio
    async def test_call_next_and_handle_error_keepHeadersOnError_false(self):
        middleware = cors({'keepHeadersOnError': False})
        ctx = mock_ctx({'Origin': 'x'})
        class CustomError(Exception): pass
        async def next_func():
            raise CustomError('fail')
        with pytest.raises(CustomError) as excinfo:
            await middleware(ctx, next_func)
        assert str(excinfo.value) == 'fail'

    @pytest.mark.asyncio
    async def test_attach_headers_to_error_when_keepHeadersOnError_true(self):
        middleware = cors({'keepHeadersOnError': True})
        ctx = mock_ctx({'Origin': 'x'})
        class E(Exception):
            def __init__(self, msg):
                super().__init__(msg)
                self.headers = {'Foo': 'Bar', 'Vary': 'X'}
        async def fake_next():
            raise E('boom')
        try:
            await middleware(ctx, fake_next)
            assert False, "Should raise"
        except Exception as e:
            assert e.headers['Foo'] == 'Bar'
            assert e.headers['Access-Control-Allow-Origin'] == '*'
            assert 'Origin' in e.headers['vary'] or 'Origin' in e.headers['Vary']
            assert e.headers.get('Vary') is None

    @pytest.mark.asyncio
    async def test_options_missing_access_control_request_method(self):
        middleware = cors()
        ctx = mock_ctx({'Origin': 'z'}, 'OPTIONS')
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert 'Access-Control-Allow-Origin' not in ctx._headers
        assert called['flag']

    @pytest.mark.asyncio
    async def test_set_preflight_headers(self):
        middleware = cors({
            'origin': 'http://a.com',
            'allowMethods': ['GET', 'DELETE'],
            'allowHeaders': ['X', 'Y'],
            'maxAge': 100,
            'credentials': True,
            'privateNetworkAccess': True
        })
        ctx = mock_ctx(
            {
                'Origin': 'http://here',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'X,Y',
                'Access-Control-Request-Private-Network': '?1'
            },
            'OPTIONS'
        )
        called = {'flag': False}
        async def next_func():
            called['flag'] = True
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Origin'] == 'http://a.com'
        assert ctx._headers['Access-Control-Allow-Methods'] == 'GET,DELETE'
        assert ctx._headers['Access-Control-Allow-Headers'] == 'X,Y'
        assert ctx._headers['Access-Control-Max-Age'] == '100'
        assert ctx._headers['Access-Control-Allow-Credentials'] == 'true'
        assert ctx._headers['Access-Control-Allow-Private-Network'] == 'true'
        assert ctx._headers['Vary'] == 'Origin'
        assert called['flag'] == False

    @pytest.mark.asyncio
    async def test_default_allowMethods(self):
        middleware = cors()
        ctx = mock_ctx(
            {
                'Origin': 'http://z',
                'Access-Control-Request-Method': 'PUT'
            },
            'OPTIONS'
        )
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Allow-Methods'] == 'GET,HEAD,PUT,POST,DELETE,PATCH'

    @pytest.mark.asyncio
    async def test_allowHeaders_as_undefined(self):
        middleware = cors()
        ctx = mock_ctx(
            {
                'Origin': 'http://o',
                'Access-Control-Request-Method': 'POST'
            },
            'OPTIONS'
        )
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert 'Access-Control-Allow-Headers' not in ctx._headers

    @pytest.mark.asyncio
    async def test_not_set_ac_allow_private_network_if_not_requested(self):
        middleware = cors({'privateNetworkAccess': True})
        ctx = mock_ctx(
            {
                'Origin': 'http://o',
                'Access-Control-Request-Method': 'POST'
            }, 'OPTIONS'
        )
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert 'Access-Control-Allow-Private-Network' not in ctx._headers

    @pytest.mark.asyncio
    async def test_not_set_credentials_unless_requested(self):
        middleware = cors({'credentials': False})
        ctx = mock_ctx(
            {
                'Origin': 'http://o',
                'Access-Control-Request-Method': 'GET'
            },
            'OPTIONS'
        )
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert 'Access-Control-Allow-Credentials' not in ctx._headers

    @pytest.mark.asyncio
    async def test_handle_maxAge_string_and_number(self):
        middleware = cors({'maxAge': 999})
        ctx = mock_ctx({'Origin': 'yo', 'Access-Control-Request-Method': 'P'}, 'OPTIONS')
        async def next_func():
            pass
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Max-Age'] == '999'
        middleware = cors({'maxAge': '123'})
        ctx = mock_ctx({'Origin': 'yo', 'Access-Control-Request-Method': 'P'}, 'OPTIONS')
        await middleware(ctx, next_func)
        assert ctx._headers['Access-Control-Max-Age'] == '123'

    @pytest.mark.asyncio
    async def test_default_keepHeadersOnError_true(self):
        middleware = cors()
        ctx = mock_ctx({'Origin': 'y'})
        class E(Exception):
            def __init__(self, msg):
                super().__init__(msg)
                self.headers = {}
        async def fake_next():
            raise E('kaboom')
        try:
            await middleware(ctx, fake_next)
            assert False, "Should raise"
        except Exception as e:
            assert e.headers['Access-Control-Allow-Origin'] == '*'
            assert 'Origin' in e.headers['vary'] or 'Origin' in e.headers['Vary']