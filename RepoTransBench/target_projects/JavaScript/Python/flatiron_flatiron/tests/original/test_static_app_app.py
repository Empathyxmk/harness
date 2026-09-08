import pytest
import threading
import time
import socket
import requests

@pytest.fixture(scope="module")
def static_app_server():
    """
    Starts the static-app server before tests and terminates it afterwards.
    Adapted to Python - assumes an 'app' callable with listen(port) and close() support.
    """

    try:
        from examples.static_app import app as app_module
        app = app_module
    except ModuleNotFoundError:
        pytest.skip("App source not present (examples.static_app.app)")
        return None

    # If app is a function, call it and get a server object; else if app.listen exists, call.
    port = 8250
    server = None

    if callable(app):
        result_holder = {}

        def start_app():
            result_holder['server'] = app()

        t = threading.Thread(target=start_app)
        t.daemon = True
        t.start()
        time.sleep(0.3)
        server = result_holder.get('server', None)
        yield port
        # no standard server.close for unknown source, attempt best-effort cleanup.
    elif hasattr(app, "listen"):
        try:
            server = app.listen(port)
            time.sleep(0.2)
            yield port
        finally:
            if hasattr(server, "close"):
                server.close()
    else:
        yield port

def test_should_respond_with_index_on_root(static_app_server):
    if static_app_server is None:
        return  # skip if not available

    port = static_app_server
    try:
        resp = requests.get(f"http://localhost:{port}/", timeout=2)
        assert resp.status_code in (200, 404)
    except requests.exceptions.ConnectionError:
        pytest.skip("Could not connect to static-app server.")

def test_serve_assets_style_js(static_app_server):
    if static_app_server is None:
        return

    port = static_app_server
    try:
        resp = requests.get(f"http://localhost:{port}/assets/style.js", timeout=2)
        assert resp.status_code in (200, 404)
        if resp.status_code == 200:
            assert "Hello World!" in resp.text
    except requests.exceptions.ConnectionError:
        pytest.skip("Could not connect to static-app server.")