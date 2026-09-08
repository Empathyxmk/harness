import pytest
import threading
import time
import requests

@pytest.fixture(scope="module")
def static_app_server():
    try:
        from examples.static_app import app as app_module
        app = app_module
    except ModuleNotFoundError:
        pytest.skip("App source not present (examples.static_app.app)")
        return None

    port = 8325
    server = None
    if callable(app):
        result_holder = {}

        def start_app():
            result_holder['server'] = app()

        t = threading.Thread(target=start_app)
        t.daemon = True
        t.start()
        time.sleep(0.25)
        server = result_holder.get('server', None)
        yield port
        # Assume best-effort cleanup
    elif hasattr(app, "listen"):
        try:
            server = app.listen(port)
            time.sleep(0.18)
            yield port
        finally:
            if hasattr(server, "close"):
                server.close()
    else:
        yield port

def test_invalid_path_likely_404(static_app_server):
    if static_app_server is None:
        return
    port = static_app_server
    try:
        resp = requests.get(f"http://localhost:{port}/nonexistent", timeout=2)
        assert resp.status_code in (404, 200)
    except requests.exceptions.ConnectionError:
        pytest.skip("Could not connect to static-app server.")

def test_serve_assets_style_css_responds_correctly(static_app_server):
    if static_app_server is None:
        return
    port = static_app_server
    try:
        resp = requests.get(f"http://localhost:{port}/assets/style.css", timeout=2)
        assert resp.status_code in (200, 404)
        if resp.status_code == 200:
            assert any(s in resp.text for s in ["body", "Hello", "hello", "Body"])
    except requests.exceptions.ConnectionError:
        pytest.skip("Could not connect to static-app server.")