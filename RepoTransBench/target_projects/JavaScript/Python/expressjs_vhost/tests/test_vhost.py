import pytest
import re
import json
from src.vhost import vhost

def create_server(hostname, handler=None):
    """
    Create a minimal server interface similar to Node.js test code.
    This will be called with instanced vhost objects, or hostname/handler directly.
    """
    vhosts = None
    if isinstance(hostname, list):
        vhosts = hostname
    else:
        vhosts = [vhost(hostname, handler)]
    # "server" will be a handler-like object that takes (method, path, headers)
    # and returns (status, response_body)
    def server(method, path, headers):
        req = {'method': method, 'path': path, 'headers': headers, 'vhost': None}
        res = {}
        index = 0
        def next_func(err=None):
            nonlocal index
            if err is not None:
                res['status'] = getattr(err, 'status', 500)
                res['body'] = str(err)
                return res
            if index >= len(vhosts):
                res['status'] = 404
                res['body'] = 'no vhost for "{}"'.format(headers.get('host'))
                return res
            handler = vhosts[index]
            index += 1
            # handler may call next_func
            return handler(req, res, next_func)
        response = next_func()
        # Handler may update res in-place
        if isinstance(response, dict) and 'status' in response and 'body' in response:
            return response['status'], response['body']
        if 'status' in res and 'body' in res:
            return res['status'], res['body']
        # default
        return 200, res.get('body', '')
    return server

def test_should_route_by_host():
    def tobi(req, res):
        res['status'] = 200
        res['body'] = 'tobi'
        return res
    def loki(req, res):
        res['status'] = 200
        res['body'] = 'loki'
        return res
    vhosts = [
        vhost('tobi.com', tobi),
        vhost('loki.com', loki)
    ]
    app = create_server(vhosts)
    status, body = app('GET', '/', {'host': 'tobi.com'})
    assert status == 200
    assert body == 'tobi'

def test_should_ignore_port_in_host():
    def handler(req, res):
        res['status'] = 200
        res['body'] = 'tobi'
        return res
    app = create_server('tobi.com', handler)
    status, body = app('GET', '/', {'host': 'tobi.com:8080'})
    assert status == 200
    assert body == 'tobi'

def test_should_support_ipv6_literal_in_host():
    def handler(req, res):
        res['status'] = 200
        res['body'] = 'loopback'
        return res
    app = create_server('[::1]', handler)
    status, body = app('GET', '/', {'host': '[::1]:8080'})
    assert status == 200
    assert body == 'loopback'

def test_should_404_unless_matched():
    def tobi(req, res):
        res['status'] = 200
        res['body'] = 'tobi'
        return res
    def loki(req, res):
        res['status'] = 200
        res['body'] = 'loki'
        return res
    vhosts = [vhost('tobi.com', tobi), vhost('loki.com', loki)]
    app = create_server(vhosts)
    status, body = app('GET', '/', {'host': 'ferrets.com'})
    assert status == 404

def test_should_404_without_host_header():
    def tobi(req, res):
        res['status'] = 200
        res['body'] = 'tobi'
        return res
    def loki(req, res):
        res['status'] = 200
        res['body'] = 'loki'
        return res
    vhosts = [vhost('tobi.com', tobi), vhost('loki.com', loki)]
    app = create_server(vhosts)
    # Simulate missing host header
    status, body = app('GET', '/', {})
    assert status == 404
    assert body == 'no vhost for "None"'

class DummyException(Exception):
    pass

class TestArguments:
    def test_hostname_required(self):
        with pytest.raises(TypeError):
            vhost()
    def test_should_accept_string(self):
        v = vhost('loki.com', lambda req, res: None)
        assert v is not None
    def test_should_accept_regexp(self):
        regex = re.compile('loki\\.com')
        v = vhost(regex, lambda req, res: None)
        assert v is not None

class TestArgumentsHandle:
    def test_handle_required(self):
        with pytest.raises(TypeError):
            vhost('loki.com')
    def test_should_accept_function(self):
        v = vhost('loki.com', lambda req, res: None)
        assert v is not None
    def test_should_reject_plain_object(self):
        with pytest.raises(TypeError):
            vhost('loki.com', {})

class TestWithStringHostname:
    def test_should_support_wildcards(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'wildcard!'
            return res
        app = create_server('*.ferrets.com', handler)
        status, body = app('GET', '/', {'host': 'loki.ferrets.com'})
        assert status == 200
        assert body == 'wildcard!'

    def test_should_restrict_wildcards_to_single_part(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'wildcard!'
            return res
        app = create_server('*.ferrets.com', handler)
        status, body = app('GET', '/', {'host': 'foo.loki.ferrets.com'})
        assert status == 404

    def test_should_treat_dot_as_dot(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'tobi'
            return res
        app = create_server('a.b.com', handler)
        status, body = app('GET', '/', {'host': 'aXb.com'})
        assert status == 404

    def test_should_match_entire_string(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'commercial'
            return res
        app = create_server('.com', handler)
        status, body = app('GET', '/', {'host': 'foo.com'})
        assert status == 404

    def test_should_populate_req_vhost(self):
        def handler(req, res):
            keys = sorted(req['vhost'].keys())
            arr = [ [k, req['vhost'][k]] for k in keys ]
            res['status'] = 200
            res['body'] = json.dumps(arr)
            return res
        app = create_server('user-*.*.com', handler)
        status, body = app('GET', '/', {'host': 'user-bob.foo.com:8080'})
        assert status == 200
        assert json.loads(body) == [
            ["0", "bob"], ["1", "foo"],
            ["host", "user-bob.foo.com:8080"],
            ["hostname", "user-bob.foo.com"], ["length", 2]
        ]

class TestWithRegexpHostname:
    def test_should_match_using_regexp(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'tobi'
            return res
        regex = re.compile(r'[tl]o[bk]i\.com')
        app = create_server(regex, handler)
        status, body = app('GET', '/', {'host': 'toki.com'})
        assert status == 200
        assert body == 'tobi'

    def test_should_match_entire_hostname(self):
        def tobi(req, res):
            res['status'] = 200
            res['body'] = 'tobi'
            return res
        def loki(req, res):
            res['status'] = 200
            res['body'] = 'loki'
            return res
        vhosts = [vhost(re.compile(r'\.tobi$'), tobi), vhost(re.compile(r'^loki\.'), loki)]
        app = create_server(vhosts)
        status, body = app('GET', '/', {'host': 'loki.tobi.com'})
        assert status == 404

    def test_should_populate_req_vhost(self):
        def handler(req, res):
            keys = sorted(req['vhost'].keys())
            arr = [ [k, req['vhost'][k]] for k in keys ]
            res['status'] = 200
            res['body'] = json.dumps(arr)
            return res
        regex = re.compile(r'user-(bob|joe)\.([^.]+)\.com')
        app = create_server(regex, handler)
        status, body = app('GET', '/', {'host': 'user-bob.foo.com:8080'})
        assert status == 200
        assert json.loads(body) == [
            ["0", "bob"], ["1", "foo"],
            ["host", "user-bob.foo.com:8080"],
            ["hostname", "user-bob.foo.com"], ["length", 2]
        ]