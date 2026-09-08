import pytest
import json
from flask import Flask, request, Response
from freezegun import freeze_time
from datetime import timedelta, datetime

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
                if whitelist is not None and whitelist():
                    return None
                if callable(lookup):
                    class Opt:
                        pass
                    opts_copy = {"lookup": lookup, "total": total, "expire": expire}
                    def next_func():
                        pass
                    lookup(flask_request, None, opts_copy, next_func)
                    real_lookup = opts_copy.get('lookup')
                    real_total = opts_copy.get('total', total)
                else:
                    real_lookup = lookup
                    real_total = total
                if isinstance(real_lookup, str):
                    val = None
                    if real_lookup == "ip":
                        val = flask_request.remote_addr or "2.3.4.5"
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
                        val = getattr(flask_request, real_lookup, "2.3.4.5")
                else:
                    val = "2.3.4.5"

                key = f"lim_{real_lookup}_{val}"
                now = datetime.now().timestamp() * 1000
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
                        "remaining": real_total - 1,
                        "reset": now + expire
                    }
                    redis.set(key, json.dumps(state), None, expire)
                else:
                    state = red_val
                    if state['remaining'] > 0:
                        state['remaining'] -= 1
                        redis.set(key, json.dumps(state), None, expire)
                    else:
                        state['remaining'] = 0
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

def test_should_call_whitelist_bypass_public(limiter_setup):
    app, redis, limiter = limiter_setup
    from unittest.mock import MagicMock
    whitelist = MagicMock(return_value=True)
    mw = limiter({
        "lookup": "headers.x-real-ip",
        "total": 2,
        "expire": 500,
        "whitelist": whitelist
    })()
    spy = MagicMock()
    with app.test_request_context("/", headers={'x-real-ip': '2.3.4.5'}):
        req = request
        res = None
        next_func = spy
        result = mw(lambda: None)
        whitelist.assert_called()
        spy.assert_not_called()

def test_should_handle_lookup_as_string_query_param(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/x",
        "method": "post",
        "lookup": "query.user",
        "total": 3,
        "expire": 700
    })
    @app.route("/x", methods=["POST"])
    @mw
    def test_x():
        return '', 201

    with app.test_client() as client:
        response = client.post("/x", query_string={"user": "john"})
        assert response.status_code == 201

def test_should_use_default_onRateLimited_with_new_path(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/y",
        "method": "put",
        "lookup": "ip",
        "total": 1,
        "expire": 600
    })
    @app.route("/y", methods=["PUT"])
    @mw
    def test_y():
        return '', 200

    with app.test_client() as client:
        response = client.put("/y")
        assert response.status_code == 200
        response2 = client.put("/y")
        assert response2.status_code == 429
        assert b"Rate limit exceeded" in response2.data

def test_should_handle_onRateLimited_override_public(limiter_setup):
    app, redis, limiter = limiter_setup
    def custom(req, res, next_):
        return Response("public custom", status=429)
    mw = limiter({
        "path": "/z",
        "method": "delete",
        "lookup": "ip",
        "total": 2,
        "expire": 800,
        "onRateLimited": custom
    })
    @app.route("/z", methods=["DELETE"])
    @mw
    def test_z():
        return '', 204

    with app.test_client() as client:
        response1 = client.delete("/z")
        assert response1.status_code == 204
        response2 = client.delete("/z")
        assert response2.status_code == 204
        response3 = client.delete("/z")
        assert response3.status_code == 429
        assert b"public custom" in response3.data

def test_should_not_set_headers_skipheaders_public(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/skip2",
        "method": "get",
        "lookup": "ip",
        "total": 1,
        "expire": 520,
        "skipHeaders": True
    })
    @app.route("/skip2", methods=["GET"])
    @mw
    def test_skip2():
        return '', 200

    with app.test_client() as client:
        response1 = client.get("/skip2")
        assert response1.status_code == 200
        response2 = client.get("/skip2")
        assert response2.status_code == 429
        assert "x-ratelimit-limit" not in response2.headers
        assert "x-ratelimit-remaining" not in response2.headers

def test_should_handle_expired_limit_and_reset_public(monkeypatch, limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "path": "/reset2",
        "method": "get",
        "lookup": "ip",
        "total": 2,
        "expire": 900
    })
    @app.route("/reset2", methods=["GET"])
    @mw
    def test_reset2():
        return '', 200

    with freeze_time() as frozen:
        with app.test_client() as client:
            response1 = client.get("/reset2")
            assert response1.status_code == 200
            response2 = client.get("/reset2")
            assert response2.status_code == 200
            frozen.tick(delta=timedelta(milliseconds=1000))
            response3 = client.get("/reset2")
            assert response3.status_code == 200

def test_should_handle_ignoreerrors_with_redis_error_public(monkeypatch):
    class BrokenRedis:
        def get(self, key):
            raise Exception("public_fail")
        def set(self, key, val, px, expire, cb=None):
            pass
    app = Flask(__name__)
    limiter = limiter_factory(BrokenRedis())
    mw = limiter({
        "path": "/err2",
        "method": "post",
        "lookup": "ip",
        "total": 2,
        "expire": 750,
        "ignoreErrors": True
    })
    @app.route("/err2", methods=["POST"])
    @mw
    def test_err2():
        return 'ok2'

    with app.test_client() as client:
        response = client.post("/err2")
        assert b"ok2" in response.data
        assert response.status_code == 200

def test_should_handle_method_path_undefined_middleware_public(limiter_setup):
    app, redis, limiter = limiter_setup
    mw = limiter({
        "lookup": "headers.x-custom-ip",
        "total": 5,
        "expire": 600
    })
    assert callable(mw())

def test_should_support_lookup_function_new_req_public(limiter_setup):
    app, redis, limiter = limiter_setup
    def lookup_func(flask_req, res, opts, next_):
        flask_req.lim_ip = '6.7.8.9'
        opts['lookup'] = 'lim_ip'
        opts['total'] = 1
        next_()
    mw = limiter({
        "path": "/func2",
        "method": "put",
        "lookup": lookup_func,
        "total": 5,
        "expire": 1000
    })
    @app.route("/func2", methods=["PUT"])
    @mw
    def test_func2():
        return '', 200

    with app.test_client() as client:
        response = client.put("/func2")
        assert response.status_code == 200

def test_should_not_allow_negative_limit_remaining_public(limiter_setup):
    app, redis, limiter = limiter_setup
    def evil_get(key):
        return json.dumps({"total": 2, "remaining": 0, "reset": (datetime.now().timestamp() * 1000) + 2000})
    redis.get = evil_get

    mw = limiter({
        "path": "/neg2",
        "method": "get",
        "lookup": "ip",
        "total": 2,
        "expire": 2000
    })
    @app.route("/neg2", methods=["GET"])
    @mw
    def test_neg2():
        return '', 200

    with app.test_client() as client:
        response = client.get("/neg2")
        assert response.status_code == 429