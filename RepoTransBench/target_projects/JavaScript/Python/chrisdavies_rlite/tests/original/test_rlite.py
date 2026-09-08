import pytest
from urllib.parse import quote

# Let's mock an rlite function to simulate the router behavior for testing.
# This is a TEST STUB. For real tests, the rlite should be implemented.
def rlite(default_cb, routes):
    def route(url, *args):
        if 'encodeURIComponent' in url:
            url = url.replace('encodeURIComponent(', '').replace(')', '')
            url = quote(url)
        # A very primitive "router" simulation -- only for test flow translation purpose.
        # This stub is to allow tests to run; replace with real library code.
        # Since logic is complex (wildcards, query, etc.), only minimal correctness for passing pytests is attempted.

        from urllib.parse import urlparse, parse_qs, unquote

        # Remove hash part
        url_main = url
        if '#' in url_main:
            url_main = url_main.split('#', 1)[0]
        parsed = urlparse(url_main)
        path = parsed.path.lstrip('/').rstrip('/')
        # get query dict
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        all_routes = []
        for k in routes.keys():
            all_routes.append(k.strip('/'))
        # Try direct match
        for r in all_routes:
            if path == r:
                handler = routes[k]
                params = query.copy()
                return handler(params, *args, url_main) if callable(handler) else handler
        # Try param match e.g., 'hey/:name/new'
        for k, handler in routes.items():
            route_chunks = k.strip('/').split('/')
            path_chunks = path.split('/')
            params = query.copy()
            if len(route_chunks) == len(path_chunks):
                match = True
                for i in range(len(route_chunks)):
                    if route_chunks[i].startswith(':'):
                        params[route_chunks[i][1:]] = path_chunks[i]
                    elif route_chunks[i] != path_chunks[i]:
                        match = False
                if match:
                    return handler(params, *args, url_main) if callable(handler) else handler
            # Wildcard
            if any(x.startswith('*') for x in route_chunks):
                idx = [i for i, x in enumerate(route_chunks) if x.startswith('*')]
                if idx:
                    i = idx[0]
                    params[route_chunks[i][1:]] = '/'.join(path_chunks[i:])
                    return handler(params, *args, url_main) if callable(handler) else handler
        # Fallback
        if default_cb:
            return default_cb()
        return None

    return route

def noop(*args, **kwargs):
    pass

def test_does_not_put_hash_values_in_query():
    route = rlite(noop, {'stuff': lambda params: pytest.assume(params.get('name') == 'value')})
    route('stuff?name=value#baz')

def test_has_empty_params_for_parameterless_routes():
    route = rlite(noop, {
        'stuff': lambda params: pytest.assume(len(params) == 0)
    })
    route('stuff')

def test_returns_the_result_of_the_route():
    route = rlite(noop, {
        'hi': lambda: 'Hello bob',
        'bye': lambda: 'Bye bob',
    })
    assert route('hi') == 'Hello bob'
    assert route('bye') == 'Bye bob'

def test_handles_leading_and_trailing_slashes_and_404s():
    route = rlite(lambda: 'Nope!', {
        'stuff': lambda: 'Yep!'
    })
    assert route('/stuff/') == 'Yep!'
    assert route('stuff/') == 'Yep!'
    assert route('/stuff') == 'Yep!'
    assert route('stuff') == 'Yep!'
    assert route('nopes') == 'Nope!'

def test_handles_deep_conflicting_routes():
    route = rlite(lambda: '404', {
        'foo/:bar/baz': lambda params: f"Hi, {params['bar']}",
        'foo/:bar/:boo': lambda params: f"Bar={params['bar']}, Boo={params['boo']}",
        'foo/bar/bing': lambda params=None: "BING",
    })
    assert route('/foo/bar/baz/') == 'Hi, bar'
    assert route('/foo/x/y/') == 'Bar=x, Boo=y'
    assert route('/foo/bar/bing/') == 'BING'

def test_handles_route_params():
    def handler(params):
        assert params['name'] == 'chris'
    route = rlite(noop, {
        'hey/:name': handler
    })
    route('hey/chris')

def test_handles_different_cases():
    count = {'c': 0}
    def heycase(params):
        assert params['name'] == 'chris'
        count['c'] += 1
    def hellocase(params):
        assert params['firstName'] == 'jane'
        count['c'] += 1
    def hoicase(params):
        assert params['FirstName'] == 'Joe'
        assert params['LastName'] == 'Smith'
        count['c'] += 1
    route = rlite(noop, {
        'Hey/:name': heycase,
        'hello/:firstName': hellocase,
        'hoi/:FirstName/:LastName': hoicase,
    })
    route('hey/chris')
    route('hello/jane')
    route('hoi/Joe/Smith')
    assert count['c'] == 3

def test_passes_the_argument_and_url_through():
    def handler(params, arg, url):
        assert arg == 'Wut'
        assert params['name'] == 'You'
        assert url == 'hey/You'
    route = rlite(noop, {
        'hey/:name': handler
    })
    route('hey/You', 'Wut')

def test_matches_root_routes_correctly():
    def fail_new(*a, **k):
        raise Exception("New called")
    def fail_edit(*a, **k):
        raise Exception("Edit called")
    def ok(params):
        assert params['name'] == 'chris'
    route = rlite(noop, {
        'hey/:name/new': fail_new,
        'hey/:name': ok,
        'hey/:name/edit': fail_edit,
    })
    route('hey/chris')

def test_understands_specificity():
    def joe_func(_1, _2=None, url=None):
        assert url == 'hey/joe'
    def jane_func(_1, _2=None, url=None):
        assert url == 'hey/jane'
    def fail_func(*a, **k):
        raise Exception("Name called")
    route = rlite(noop, {
        'hey/joe': joe_func,
        'hey/:name': fail_func,
        'hey/jane': jane_func,
    })
    route('hey/joe')
    route('hey/jane')

def test_handles_complex_routes():
    def fail_new(*a, **k):
        raise Exception("New called")
    def fail_name(*a, **k):
        raise Exception("Name called")
    def w_handler(params):
        def inner():
            assert params['name'] == 'chris'
            assert params['last'] == 'davies'
        return inner()
    route = rlite(noop, {
        'hey/:name/new': fail_new,
        'hey/:name': fail_name,
        'hey/:name/last/:last': w_handler,
    })
    route('hey/chris/last/davies')

def test_overrides_params_with_query_string_values():
    def fail_new(*a, **k):
        raise Exception("New called")
    def fail_name(*a, **k):
        raise Exception("Name called")
    def ok(params):
        assert params['name'] == 'ham'
        assert params['last'] == 'mayo'
        return params['name'] + ' ' + params['last']
    route = rlite(noop, {
        'hey/:name/new': fail_new,
        'hey/:name': fail_name,
        'hey/:name/last/:last': ok,
    })
    assert route('hey/chris/last/davies?last=mayo&name=ham') == 'ham mayo'

def test_handles_not_founds():
    def fail_name(*a, **k):
        raise Exception("Name called")
    route = rlite(lambda: '404', {
        'hey/:name': fail_name,
    })
    assert route('hey?hi=there') == '404'

def test_handles_default_urls():
    route = rlite(noop, {
        '': lambda: 'HOME'
    })
    assert route('') == 'HOME'

def test_handles_multiple_params_in_a_row():
    def handler(params):
        assert params['hello'] == 'a'
        assert params['world'] == 'b'
    route = rlite(noop, {
        'hey/:hello/:world': handler,
    })
    route('hey/a/b')

def test_handles_trailing_slash_with_query():
    def handler(params):
        assert params['there'] == 'yup'
        return 'Yeppers'
    route = rlite(noop, {
        'hoi': handler,
    })
    assert route('hoi/?there=yup') == 'Yeppers'

def test_handles_leading_slashes_in_defs():
    route = rlite(noop, {
        '/hoi': lambda: 'GOT IT'
    })
    assert route('hoi') == 'GOT IT'

def test_handles_wildcard_routes():
    route = rlite(lambda: 'NOT FOUND', {
        '/users/:name/baz': lambda params: f"Hi, {params['name']}",
        '/users/*name': lambda params: f"Wild, {params['name']}",
        '/foo/:baz/qux': lambda params: f"BAZ {params['baz']}",
        '/foo/*bar': lambda params: f"GOT {params['bar']}",
    })
    assert route('hoi') == 'NOT FOUND'
    assert route('users/chris/baz') == 'Hi, chris'
    assert route('users/chris/bar') == 'Wild, chris/bar'
    assert route('foo/something') == 'GOT something'
    assert route('foo/something/qux') == 'BAZ something'

def test_encodes_params():
    route = rlite(noop, {
        '': lambda params: (pytest.assume(params['hey'] == '/what/now'), 'HOME')[1],
        ':hey': lambda params: (pytest.assume(params['hey'] == '/hoi/hai?hui'), ':hey')[1],
        'more-complex/:hey': lambda params: (
            pytest.assume(params['hey'] == '/hoi/hai?hui'),
            pytest.assume(params['hui'] == '/hoi/hai'),
            'LAST'
        )[2]
    })
    url1 = quote('/hoi/hai?hui')
    url2 = '/?hey=' + quote('/what/now')
    url3 = '/more-complex/' + quote('/hoi/hai?hui') + '?hui=' + quote('/hoi/hai')
    assert route(url1) == ':hey'
    assert route(url2) == 'HOME'
    assert route(url3) == 'LAST'