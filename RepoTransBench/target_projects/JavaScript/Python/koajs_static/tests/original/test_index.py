import os
import pytest

def _has_text_index():
    return os.path.isfile("test/fixtures/index.txt")

def _has_html_index():
    return os.path.isfile("test/fixtures/world/index.html")

@pytest.mark.parametrize("defer_option", [False, True])
def test_root_missing_raises(defer_option):
    from src.koajs_static import serve
    with pytest.raises(ValueError, match="root directory is required to serve files"):
        serve()

def test_should_serve_from_cwd(monkeypatch):
    # only makes sense if package.json exists in cwd during test run
    from src.koajs_static import serve, create_koa_like_app
    import requests
    import pathlib
    app = create_koa_like_app('.', serve_kwargs={})
    # We'll assume package.json exists in the current dir
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/package.json'
        r = requests.get(url)
        assert r.status_code == 200

def test_should_404_for_missing_file():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/something'
        r = requests.get(url)
        assert r.status_code == 404

def test_should_not_throw_404_error():
    from src.koajs_static import create_koa_like_app
    import requests
    downstream_ok = []
    app = create_koa_like_app('test/fixtures', extra_middleware=lambda req: downstream_ok.append(True))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/something'
        r = requests.get(url)
        assert r.status_code == 200
        assert downstream_ok
        assert r.text == 'ok'

def test_upstream_middleware_responds():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', extra_middleware=lambda req: req.set_response('hey'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/hello.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'world'

def test_the_path_is_valid():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/hello.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'world'

def test_index_present():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'index': 'index.txt'})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'text index'
        assert r.headers['content-type'] == 'text/plain; charset=utf-8'

def test_index_omitted():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/world/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'html index'
        assert r.headers['content-type'] == 'text/html; charset=utf-8'

def test_index_disabled():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'index': False})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/world/'
        r = requests.get(url)
        assert r.status_code == 404

def test_index_disabled_downstream():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'index': False}, extra_middleware=lambda req: req.set_response('oh no'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/world/'
        r = requests.get(url)
        assert r.text == 'oh no'

@pytest.mark.parametrize("method", ['POST', 'PUT', 'DELETE'])
def test_method_not_get_or_head(method):
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/hello.txt'
        r = requests.request(method, url)
        assert r.status_code == 404

# Defer: true test group emulated below (using serve_kwargs={"defer": True} etc)

def test_defer_upstream_middleware_responds():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True},
                              extra_middleware=lambda req: req.set_response('hey'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/hello.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'hey'

def test_defer_the_path_is_valid():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/hello.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'world'

def test_defer_not_valid():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/something'
        r = requests.get(url)
        assert r.status_code == 404

def test_defer_not_throw_404():
    from src.koajs_static import create_koa_like_app
    import requests
    downstream_ok = []
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True},
                              extra_middleware=lambda req: downstream_ok.append(True) or req.set_response('ok'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/something'
        r = requests.get(url)
        assert downstream_ok
        assert r.text == 'ok'
        assert r.status_code == 200

def test_defer_index_present():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True, 'index': 'index.txt'})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'text index'
        assert r.headers['content-type'] == 'text/plain; charset=utf-8'

def test_defer_index_omitted():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'html index'
        assert r.headers['content-type'] == 'text/html; charset=utf-8'

def test_defer_index_disabled():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True, 'index': False})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 404

def test_defer_index_disabled_downstream():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True, 'index': False},
                              extra_middleware=lambda req: req.set_response('oh no'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.text == 'oh no'

@pytest.mark.parametrize("method", ['POST', 'PUT'])
def test_defer_method_not_get_or_head(method):
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/index.html'
        r = requests.request(method, url)
        assert r.status_code == 404