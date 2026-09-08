import os
import pytest

def test_should_serve_hello_txt():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/hello.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'world'

def test_should_404_when_path_nonexistent():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/nonexistentfile.html'
        r = requests.get(url)
        assert r.status_code == 404

def test_should_not_throw_404_error_diff_file():
    from src.koajs_static import create_koa_like_app
    import requests
    downstream_ok = []
    app = create_koa_like_app('test/fixtures/world', extra_middleware=lambda req: downstream_ok.append(True) or req.set_response('ok-alt'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/nonexistentfile.html'
        r = requests.get(url)
        assert downstream_ok
        assert r.status_code == 200
        assert r.text == 'ok-alt'

def test_upstream_middleware_responds_diff_file():
    from src.koajs_static import create_koa_like_app
    import requests
    # Use a file that does not exist so middleware responds
    app = create_koa_like_app('test/fixtures', extra_middleware=lambda req: req.set_response('different-hey'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/nonexistent-hey.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'different-hey'

def test_the_path_is_valid_index_txt():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/index.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'text index'

def test_index_present_world_html():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'index': 'index.html'})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'html index'
        assert r.headers['content-type'] == 'text/html; charset=utf-8'

def test_index_omitted_world():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'html index'
        assert r.headers['content-type'] == 'text/html; charset=utf-8'

def test_index_disabled_world():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'index': False})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 404

def test_index_disabled_world_downstream():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'index': False}, extra_middleware=lambda req: req.set_response('oh no-alt'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.text == 'oh no-alt'

@pytest.mark.parametrize("method", ['POST'])
def test_method_not_get_or_head_world(method):
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/index.html'
        r = requests.request(method, url)
        assert r.status_code == 404

def test_defer_upstream_middleware_responds_diff_file():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True}, extra_middleware=lambda req: req.set_response('hey-alt'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/nonexistent-alt.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'hey-alt'

def test_defer_the_path_is_valid_index_txt():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/index.txt'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'text index'

def test_defer_not_valid_no_such_file():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/no-such-file.txt'
        r = requests.get(url)
        assert r.status_code == 404

def test_defer_not_throw_404_diff_file():
    from src.koajs_static import create_koa_like_app
    import requests
    downstream_ok = []
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True}, extra_middleware=lambda req: downstream_ok.append(True) or req.set_response('ok-defer-alt'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/no-such-file.txt'
        r = requests.get(url)
        assert downstream_ok
        assert r.text == 'ok-defer-alt'
        assert r.status_code == 200

def test_defer_index_present_txt():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures', serve_kwargs={'defer': True, 'index': 'index.txt'})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'text index'
        assert r.headers['content-type'] == 'text/plain; charset=utf-8'

def test_defer_index_omitted_world_html():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == 'html index'
        assert r.headers['content-type'] == 'text/html; charset=utf-8'

def test_defer_index_disabled_world_html():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True, 'index': False})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 404

def test_defer_index_disabled_world_html_downstream():
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True, 'index': False}, extra_middleware=lambda req: req.set_response('oh no-defer-alt'))
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.text == 'oh no-defer-alt'

@pytest.mark.parametrize("method", ['PUT'])
def test_defer_method_not_get_or_head_world(method):
    from src.koajs_static import create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world', serve_kwargs={'defer': True})
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/index.html'
        r = requests.request(method, url)
        assert r.status_code == 404