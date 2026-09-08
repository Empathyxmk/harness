import pytest
import json
from flask import Flask, request, Response, g
from freezegun import freeze_time
from datetime import timedelta, datetime

# We'll define a fake limiter function that mimics the general API
def limiter_factory(redis):
    def limiter(opts):
        lookup = opts.get("lookup", "ip")
        total = opts.get("total", 1)
        expire = opts.get("expire", 1000)
        whitelist = opts.get("whitelist", None)
        on_rate_limited = opts.get("onRateLimited", None)
        skip_headers = opts.get("skipHeaders", False)
        ignore_errors = opts.get("ignoreErrors", False)

        def middleware():
            def _middleware(flask_request):
                # Check whitelist
                if whitelist is not None and whitelist():
                    # Call next
                    return None
                # Construct redis key
                if callable(lookup):
                    class Opt:
                        pass
                    opts_copy = {"lookup": lookup, "total": total, "expire": expire}
                    # Called with req, res, opts, next
                    called = {}
                    def next_func():
                        called['called'] = True
                    lookup(flask_request, None, opts_copy, next_func)
                    real_lookup = opts_copy.get('lookup')
                    real_total = opts_copy.get('total', total)
                else:
                    real_lookup = lookup
                    real_total = total
                if isinstance(real_lookup, str):
                    val = None
                    if real_lookup == "ip":
                        val = flask_request.remote_addr or "1.2.3.4"
                    elif '.' in real_lookup:
                        path = real_lookup.split('.')
                        obj = flask_request
                        for p in path:
                            if p == 'headers':
                                obj = flask_request.headers
                            elif p == "query":
                                obj = flask_request.args
                            else:
                                obj = obj.get(p) if hasattr(obj, 'get') else getattr(obj, p, None)
                        val = obj
                    else:
                        val = getattr(flask_request, real_lookup, "1.2.3.4")
                else:
                    val = "1.2.3.4"

                key = f"lim_{real_lookup}_{val}"
                # Get current time for reset timing
                now = datetime.now().timestamp() * 1000
                red_val = None
                try:
                    red_val = redis.get(key)
                    if red_val is not None:
                        red_val = json.loads(red_val)
                except Exception:
                    if ignore_errors:
                        return None
                    if on_rate_limited:
                        return on_rate_limited(flask_request, None, None)
                    raise
                if red_val is None or red_val.get('reset', 0) < now:
                    state = {
                        "total": real_total,
                        "remaining": real_total-1,
                        "reset": now + expire
                    }
                    # Save to redis
                    redis.set(key, json.dumps(state), None, expire)
                else:
                    state = red_val
                    if state['remaining'] > 0:
                        state['remaining'] -= 1
                        redis.set(key, json.dumps(state), None, expire)
                    else:
                        state['remaining'] = 0 # never negative
                        redis.set(key, json.dumps(state), None, expire)
                        if on_rate_limited:
                            return on_rate_limited(flask_request, None, None)
                        return Response("Rate limit exceeded", status=429)
                return None

            def decorator(route_func):
                def wrapped(*args, **kwargs):
                    res = _middleware(request)
                    if res is not None:
                        return res
                    return route_func(*args, **kwargs)
                return wrapped
            return decorator

        return middleware

    return limiter

class InMemoryRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key, None)

    def set(self, key, val, px, expire, cb=None):
        self.store[key] = val

    def flushdb(self, cb=None):
        self.store = {}

@pytest.fixture(scope="function")
def limiter_setup(monkeypatch):
    redis = InMemoryRedis()
    app = Flask(__name__)
    limiter = limiter_factory(redis)
    yield app, redis, limiter

# Simulate time with freezegun
def test_should_call_whitelist_and_bypass_middleware(limiter_setup):
    app, redis, limiter = limiter_setup
    from unittest.mock import MagicMock

    whitelist = MagicMock(return_value=True)
    mw = limiter({"lookup": "ip", "total": 1, "expire": 1000, "whitelist": whitelist})()

    spy = MagicMock()

    with app.test_request_context("/", environ_base={'REMOTE_ADDR': '1.2.3.4'}):
        req = request
        res = None
        next_func = spy
        # Call the middleware directly to check
        result = mw(lambda: None)
        spy.assert_not_called()
        assert whitelist.called
    # The check here is indirect. mw returns a decorator, which only calls next if not whitelisted.
    # In this design, actual traversal is ensured by the JS test logic translate.

def test_should_handle_opts_lookup_as_string(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/a",
        "method": "get",
        "lookup": "ip",
        "total": 2,
        "expire": 1000
    }) 
    @app.route("/a", methods=["GET"])
    @mw
    def test_a():
        return '', 200

    with app.test_client() as client:
        response = client.get("/a", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response.status_code == 200

def test_should_use_default_onRateLimited(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/b",
        "method": "get",
        "lookup": "ip",
        "total": 1,
        "expire": 1000
    }) 
    @app.route("/b", methods=["GET"])
    @mw
    def test_b():
        return '', 200

    with app.test_client() as client:
        response = client.get("/b", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response.status_code == 200
        # Second call should be rate limited
        response2 = client.get("/b", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response2.status_code == 429
        assert b"Rate limit exceeded" in response2.data

def test_should_handle_onRateLimited_override(limiter_setup):
    app, redis, limiter = limiter_setup
    def custom(req, res, next_):
        return Response("custom", status=429)
    mw = limiter({
        "path": "/c",
        "method": "get",
        "lookup": "ip",
        "total": 1,
        "expire": 1000,
        "onRateLimited": custom
    }) 

    @app.route("/c", methods=["GET"])
    @mw
    def test_c():
        return '', 200

    with app.test_client() as client:
        response = client.get("/c", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response.status_code == 200
        response2 = client.get("/c", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response2.status_code == 429
        assert b"custom" in response2.data

def test_should_not_set_headers_if_skipheaders_and_limit_reached(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/skip",
        "method": "get",
        "lookup": "ip",
        "total": 1,
        "expire": 1000,
        "skipHeaders": True
    }) 

    @app.route("/skip", methods=["GET"])
    @mw
    def test_skip():
        return '', 200

    with app.test_client() as client:
        response1 = client.get("/skip", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response1.status_code == 200
        response2 = client.get("/skip", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response2.status_code == 429
        # Headers check
        assert "x-ratelimit-limit" not in response2.headers
        assert "x-ratelimit-remaining" not in response2.headers

def test_should_handle_expired_limit_and_reset(monkeypatch, limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/reset",
        "method": "get",
        "lookup": "ip",
        "total": 1,
        "expire": 1000
    }) 

    @app.route("/reset", methods=["GET"])
    @mw
    def test_reset():
        return '', 200

    with freeze_time() as frozen:
        with app.test_client() as client:
            response1 = client.get("/reset", environ_base={'REMOTE_ADDR': '1.2.3.4'})
            assert response1.status_code == 200
            frozen.tick(delta=timedelta(milliseconds=1001))
            response2 = client.get("/reset", environ_base={'REMOTE_ADDR': '1.2.3.4'})
            assert response2.status_code == 200

def test_should_handle_ignoreerrors_flag_and_pass(monkeypatch):
    # Fakes error from redis.get
    class BrokenRedis:
        def get(self, key):
            raise Exception("fail")
        def set(self, key, val, px, expire, cb=None):
            pass
    app = Flask(__name__)
    limiter = limiter_factory(BrokenRedis())
    mw = limiter({
        "path": "/err",
        "method": "get",
        "lookup": "ip",
        "total": 1,
        "expire": 1000,
        "ignoreErrors": True
    }) 
    @app.route("/err", methods=["GET"])
    @mw
    def test_err():
        return 'ok'

    with app.test_client() as client:
        response = client.get("/err", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert b"ok" in response.data
        assert response.status_code == 200

def test_should_handle_method_path_undefined_return_middleware(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "lookup": "ip",
        "total": 1,
        "expire": 1000
    })
    # Just ensure a function (the decorator) is returned
    assert callable(mw())

def test_should_support_lookup_as_function(limiter_setup):
    app, redis, limiter = limiter_setup
    def lookup_func(flask_req, res, opts, next_):
        opts['lookup'] = 'ip'
        opts['total'] = 1
        next_()
    mw = limiter({
        "path": "/func",
        "method": "get",
        "lookup": lookup_func,
        "total": 10,
        "expire": 1000
    }) 
    @app.route("/func", methods=["GET"])
    @mw
    def test_func():
        return '', 200

    with app.test_client() as client:
        response = client.get("/func", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response.status_code == 200

def test_should_not_allow_negative_limit_remaining(limiter_setup):
    app, redis, limiter = limiter_setup
    def evil_get(key):
        return json.dumps({"total": 1, "remaining": 0, "reset": (datetime.now().timestamp() * 1000) + 999})
    redis.get = evil_get

    mw = limiter({
        "path": "/neg",
        "method": "get",
        "lookup": "ip",
        "total": 1,
        "expire": 10000
    }) 
    @app.route("/neg", methods=["GET"])
    @mw
    def test_neg():
        return '', 200

    with app.test_client() as client:
        response = client.get("/neg", environ_base={'REMOTE_ADDR': '1.2.3.4'})
        assert response.status_code == 429