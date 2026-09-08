import os
import pytest
import pathlib
import tempfile
import shutil

from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from urllib.request import urlopen

def start_server_in_thread(directory, handler_class=SimpleHTTPRequestHandler):
    """Helper to start an HTTP server serving a given directory."""
    cwd = os.getcwd()
    os.chdir(directory)
    server = HTTPServer(('localhost', 0), handler_class)
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    os.chdir(cwd)
    return server, thread

def test_throws_if_root_is_not_supplied():
    # In Python, let's simulate the same error as from the JS `serve()` function
    # We'll attempt to call a function without root, which should raise a ValueError
    from src.koajs_static import serve
    with pytest.raises(ValueError, match="root directory is required to serve files"):
        serve()

def test_sets_opts_root_absolute():
    from src.koajs_static import serve
    opts = {}
    serve('test/fixtures', opts)
    assert 'root' in opts
    assert opts['root'].endswith('test/fixtures')

def test_uses_default_index_if_none_provided(tmp_path):
    # We want to serve the 'test/fixtures/world' directory as an HTTP server, check index.html
    from src.koajs_static import serve, create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures/world')
    # Using a temp file for the socket
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/'
        r = requests.get(url)
        assert r.status_code == 200
        assert 'html index' in r.text

def test_handles_head_requests_like_get():
    from src.koajs_static import serve, create_koa_like_app
    import requests
    app = create_koa_like_app('test/fixtures')
    with app.run() as server:
        url = f'http://{server.host}:{server.port}/hello.txt'
        r = requests.head(url)
        assert r.status_code == 200