import pytest
import re
import json
from src.vhost import vhost

def create_server(hostname, handler=None):
    vhosts = None
    if isinstance(hostname, list):
        vhosts = hostname
    else:
        vhosts = [vhost(hostname, handler)]
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
            return handler(req, res, next_func)
        response = next_func()
        if isinstance(response, dict) and 'status' in response and 'body' in response:
            return response['status'], response['body']
        if 'status' in res and 'body' in res:
            return res['status'], res['body']
        return 200, res.get('body', '')
    return server

def test_route_by_host_different_public():
    def alice(req, res):
        res['status'] = 200
        res['body'] = 'alice'
        return res
    def bob(req, res):
        res['status'] = 200
        res['body'] = 'bob'
        return res
    vhosts = [
        vhost('alice.com', alice),
        vhost('bob.com', bob)
    ]
    app = create_server(vhosts)
    status, body = app('GET', '/', {'host': 'bob.com'})
    assert status == 200
    assert body == 'bob'

def test_ignore_port_in_host_public():
    def handler(req, res):
        res['status'] = 200
        res['body'] = 'bob'
        return res
    app = create_server('bob.com', handler)
    status, body = app('GET', '/', {'host': 'bob.com:1234'})
    assert status == 200
    assert body == 'bob'

def test_support_another_ipv6_literal_in_host():
    def handler(req, res):
        res['status'] = 200
        res['body'] = 'otherloop'
        return res
    app = create_server('[::2]', handler)
    status, body = app('GET', '/', {'host': '[::2]:1234'})
    assert status == 200
    assert body == 'otherloop'

def test_404_unless_matched_public():
    def alice(req, res):
        res['status'] = 200
        res['body'] = 'alice'
        return res
    def bob(req, res):
        res['status'] = 200
        res['body'] = 'bob'
        return res
    vhosts = [
        vhost('alice.com', alice),
        vhost('bob.com', bob)
    ]
    app = create_server(vhosts)
    status, body = app('GET', '/', {'host': 'cats.com'})
    assert status == 404

def test_404_without_host_header_public():
    def alice(req, res):
        res['status'] = 200
        res['body'] = 'alice'
        return res
    def bob(req, res):
        res['status'] = 200
        res['body'] = 'bob'
        return res
    vhosts = [
        vhost('alice.com', alice),
        vhost('bob.com', bob)
    ]
    app = create_server(vhosts)
    status, body = app('GET', '/', {})
    assert status == 404
    assert body == 'no vhost for "None"'

class TestPublicArguments:
    def test_hostname_required(self):
        with pytest.raises(TypeError):
            vhost()
    def test_should_accept_string(self):
        v = vhost('bob.com', lambda req, res: None)
        assert v is not None
    def test_should_accept_regexp(self):
        regex = re.compile('bob\\.com')
        v = vhost(regex, lambda req, res: None)
        assert v is not None

class TestPublicArgumentsHandle:
    def test_handle_required(self):
        with pytest.raises(TypeError):
            vhost('bob.com')
    def test_should_accept_function(self):
        v = vhost('bob.com', lambda req, res: None)
        assert v is not None
    def test_should_reject_plain_object(self):
        with pytest.raises(TypeError):
            vhost('bob.com', {})

class TestStringHostnamePublic:
    def test_should_support_wildcards_public(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'meow!'
            return res
        app = create_server('*.cats.com', handler)
        status, body = app('GET', '/', {'host': 'fluffy.cats.com'})
        assert status == 200
        assert body == 'meow!'

    def test_should_restrict_wildcards_public(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'meow!'
            return res
        app = create_server('*.cats.com', handler)
        status, body = app('GET', '/', {'host': 'foo.fluffy.cats.com'})
        assert status == 404

    def test_should_treat_dot_as_dot_public(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'xyz'
            return res
        app = create_server('x.y.com', handler)
        status, body = app('GET', '/', {'host': 'xXy.com'})
        assert status == 404

    def test_should_match_entire_string_public(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'organization'
            return res
        app = create_server('.org', handler)
        status, body = app('GET', '/', {'host': 'foo.org'})
        assert status == 404

    def test_should_populate_req_vhost_public(self):
        def handler(req, res):
            keys = sorted(req['vhost'].keys())
            arr = [ [k, req['vhost'][k]] for k in keys ]
            res['status'] = 200
            res['body'] = json.dumps(arr)
            return res
        app = create_server('client-*.*.org', handler)
        status, body = app('GET', '/', {'host': 'client-alice.bar.org:1234'})
        assert status == 200
        assert json.loads(body) == [
            ["0", "alice"], ["1", "bar"],
            ["host", "client-alice.bar.org:1234"],
            ["hostname", "client-alice.bar.org"], ["length", 2]
        ]

class TestRegexpHostnamePublic:
    def test_should_match_using_regexp_public(self):
        def handler(req, res):
            res['status'] = 200
            res['body'] = 'hat'
            return res
        regex = re.compile(r'[eh]at\.org')
        app = create_server(regex, handler)
        status, body = app('GET', '/', {'host': 'eat.org'})
        assert status == 200
        assert body == 'hat'

    def test_should_match_entire_hostname_public(self):
        def alice(req, res):
            res['status'] = 200
            res['body'] = 'alice'
            return res
        def bob(req, res):
            res['status'] = 200
            res['body'] = 'bob'
            return res
        vhosts = [
            vhost(re.compile(r'\.alice$'), alice),
            vhost(re.compile(r'^bob\.'), bob)
        ]
        app = create_server(vhosts)
        status, body = app('GET', '/', {'host': 'bob.alice.com'})
        assert status == 404

    def test_populate_req_vhost_public(self):
        def handler(req, res):
            keys = sorted(req['vhost'].keys())
            arr = [ [k, req['vhost'][k]] for k in keys ]
            res['status'] = 200
            res['body'] = json.dumps(arr)
            return res
        regex = re.compile(r'client-(alice|sam)\.([^.]+)\.org')
        app = create_server(regex, handler)
        status, body = app('GET', '/', {'host': 'client-alice.bar.org:1234'})
        assert status == 200
        assert json.loads(body) == [
            ["0", "alice"], ["1", "bar"],
            ["host", "client-alice.bar.org:1234"],
            ["hostname", "client-alice.bar.org"], ["length", 2]
        ]