import os
import pytest

def test_throws_if_root_is_not_supplied():
    from src.koajs_static import serve
    with pytest.raises(ValueError, match="root directory is required to serve files"):
        serve()

def test_sets_opts_root_absolute():
    from src.koajs_static import serve
    opts = {}
    import os
    serve(os.getcwd(), opts)
    assert opts['root'] == os.getcwd()

def test_uses_default_index_if_none_provided():
    from src.koajs_static import create_koa_like_app
    import requests
    # Use /world/ directory, which has index.html, instead of 'test/fixtures'
    app = create_koa_like_app('test/fixtures/world')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert 'html index' in r.text

def test_handles_head_requests_like_get():
    from src.koajs_static import create_koa_like_app
    import requests
    # Use 'index.txt' instead of 'hello.txt'
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/index.txt'
        r = requests.head(url)
        assert r.status_code == 200