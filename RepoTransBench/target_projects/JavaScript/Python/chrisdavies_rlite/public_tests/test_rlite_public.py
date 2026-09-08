import pytest
from urllib.parse import quote

def rlite(default_cb, routes):
    def route(url, *args):
        from urllib.parse import urlparse, parse_qs, unquote

        if '#' in url:
            url = url.split('#', 1)[0]
        parsed = urlparse(url)
        path = parsed.path.lstrip('/').rstrip('/')
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        all_routes = []
        for k in routes.keys():
            all_routes.append(k.strip('/'))
        for r in all_routes:
            if path == r:
                handler = routes[k]
                params = query.copy()
                return handler(params, *args, url) if callable(handler) else handler
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
                    return handler(params, *args, url) if callable(handler) else handler
            if any(x.startswith('*') for x in route_chunks):
                idx = [i for i, x in enumerate(route_chunks) if x.startswith('*')]
                if idx:
                    i = idx[0]
                    params[route_chunks[i][1:]] = '/'.join(path_chunks[i:])
                    return handler(params, *args, url) if callable(handler) else handler
        if default_cb:
            return default_cb()
        return None
    return route

def noop(*args, **kwargs):
    pass

def test_does_not_put_hash_values_in_query_public():
    route = rlite(noop, {'alpha': lambda params: pytest.assume(params.get('id') == '42')})
    route('alpha?id=42#sectionfoo')

def test_has_empty_params_for_parameterless_routes_public():
    route = rlite(noop, {
        'beta': lambda params: pytest.assume(len(params) == 0)
    })
    route('beta')

def test_returns_the_result_of_the_route_public():
    route = rlite(noop, {
        'greet': lambda: 'Hola Alice',
        'farewell': lambda: 'Adieu Bob',
    })
    assert route('greet') == 'Hola Alice'
    assert route('farewell') == 'Adieu Bob'

def test_handles_leading_trailing_slashes_and_404s_public():
    route = rlite(lambda: 'NopePublic!', {
        'delta': lambda: 'YepPublic!'
    })
    assert route('/delta/') == 'YepPublic!'
    assert route('delta/') == 'YepPublic!'
    assert route('/delta') == 'YepPublic!'
    assert route('delta') == 'YepPublic!'
    assert route('somethingelse') == 'NopePublic!'

def test_handles_deep_conflicting_routes_public():
    route = rlite(lambda: 'not:found', {
        'baz/:qux/quux': lambda params: f"Qux={params['qux']}",
        'baz/:qux/:foo': lambda params: f"Qux={params['qux']}, Foo={params['foo']}",
        'baz/qux/bar': lambda params=None: 'FoundBar',
    })
    assert route('/baz/qux/quux/') == 'Qux=qux'
    assert route('/baz/y/z/') == 'Qux=y, Foo=z'
    assert route('/baz/qux/bar/') == 'FoundBar'

def test_handles_route_params_public():
    def handler(params):
        assert params['word'] == 'example'
    route = rlite(noop, {
        'shout/:word': handler
    })
    route('shout/example')

def test_handles_different_cases_public():
    count = {'c': 0}
    def shout(params):
        assert params['word'] == 'example'
        count['c'] += 1
    def whisper(params):
        assert params['phrase'] == 'hi'
        count['c'] += 1
    def yell(params):
        assert params['Phrase'] == 'Foo'
        assert params['Other'] == 'Bar'
        count['c'] += 1
    route = rlite(noop, {
        'Shout/:word': shout,
        'whisper/:phrase': whisper,
        'Yell/:Phrase/:Other': yell
    })
    route('shout/example')
    route('whisper/hi')
    route('yell/Foo/Bar')
    assert count['c'] == 3

def test_passes_argument_and_url_through_public():
    def handler(params, arg, url):
        assert arg == 'ArgTest'
        assert params['who'] == 'Bob'
        assert url == 'call/Bob'
    route = rlite(noop, {
        'call/:who': handler
    })
    route('call/Bob', 'ArgTest')

def test_matches_root_routes_correctly_public():
    def fail_new(*a, **k):
        raise Exception("New called")
    def fail_edit(*a, **k):
        raise Exception("Edit called")
    def ok(params):
        assert params['value'] == 'baz'
    route = rlite(noop, {
        'foo/:value/new': fail_new,
        'foo/:value': ok,
        'foo/:value/edit': fail_edit,
    })
    route('foo/baz')

def test_understands_specificity_public():
    def lisa(_1, _2=None, url=None):
        assert url == 'foo/lisa'
    def sam(_1, _2=None, url=None):
        assert url == 'foo/sam'
    def fail_func(*a, **k):
        raise Exception("Person called")
    route = rlite(noop, {
        'foo/lisa': lisa,
        'foo/:person': fail_func,
        'foo/sam': sam,
    })
    route('foo/lisa')
    route('foo/sam')

def test_handles_complex_routes_public():
    def fail_new(*a, **k):
        raise Exception("New called")
    def fail_city(*a, **k):
        raise Exception("City called")
    def handler(params):
        assert params['city'] == 'springfield'
        assert params['state'] == 'illinois'
    route = rlite(noop, {
        'address/:city/new': fail_new,
        'address/:city': fail_city,
        'address/:city/state/:state': handler
    })
    route('address/springfield/state/illinois')

def test_overrides_params_with_query_string_values_public():
    def fail_new(*a, **k):
        raise Exception("New called")
    def fail_bar(*a, **k):
        raise Exception("Bar called")
    def ok(params):
        assert params['bar'] == 'cheese'
        assert params['baz'] == 'lettuce'
        return params['bar'] + ' ' + params['baz']
    route = rlite(noop, {
        'foo/:bar/new': fail_new,
        'foo/:bar': fail_bar,
        'foo/:bar/second/:baz': ok,
    })
    assert route('foo/original/second/mayon/?baz=lettuce&bar=cheese') == 'cheese lettuce'

def test_handles_not_founds_public():
    def fail_baz(*a, **k):
        raise Exception("baz called")
    route = rlite(lambda: 'notfound', {
        'bar/:baz': fail_baz
    })
    assert route('bar?bogus=val') == 'notfound'

def test_handles_default_urls_public():
    route = rlite(noop, {
        '': lambda: 'HOMEPUB'
    })
    assert route('') == 'HOMEPUB'

def test_handles_multiple_params_in_a_row_public():
    def handler(params):
        assert params['alpha'] == 'param1'
        assert params['beta'] == 'param2'
    route = rlite(noop, {
        'foo/:alpha/:beta': handler
    })
    route('foo/param1/param2')

def test_handles_trailing_slash_with_query_public():
    def handler(params):
        assert params['item'] == 'bike'
        return 'YesQuery'
    route = rlite(noop, {
        'bar': handler
    })
    assert route('bar/?item=bike') == 'YesQuery'

def test_handles_leading_slashes_in_defs_public():
    route = rlite(noop, {
        '/zigzag': lambda: 'GOTPUBLIC'
    })
    assert route('zigzag') == 'GOTPUBLIC'

def test_handles_wildcard_routes_public():
    route = rlite(lambda: 'NO MATCH', {
        '/people/:who/biz': lambda params: f"Hello {params['who']}",
        '/people/*who': lambda params: f"Wildcard {params['who']}",
        '/fruit/:kind/box': lambda params: f"FruitBox {params['kind']}",
        '/fruit/*what': lambda params: f"AllFruit {params['what']}",
    })
    assert route('people/mike/biz') == 'Hello mike'
    assert route('people/charlie/zoo') == 'Wildcard charlie/zoo'
    assert route('fruit/apple/box') == 'FruitBox apple'
    assert route('fruit/banana/blah') == 'AllFruit banana/blah'
    assert route('unknown/blah') == 'NO MATCH'