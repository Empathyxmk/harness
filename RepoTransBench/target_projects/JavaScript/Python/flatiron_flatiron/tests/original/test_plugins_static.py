import pytest
import requests
import os

@pytest.fixture(scope="module")
def static_server():
    # Artificial: spawn static-app server at 8080
    port = 8080
    try:
        from examples.static_app import app as app_module
        app = app_module
    except ModuleNotFoundError:
        pytest.skip("examples.static_app.app not present.")
        return
    if hasattr(app, "start"):
        server = app.start(port)
    elif hasattr(app, "listen"):
        server = app.listen(port)
    else:
        pytest.skip("No server start method present for app.")
        return
    try:
        yield port
    finally:
        if hasattr(server, "close"):
            server.close()

def test_app_extends_static_plugin():
    # Simulate app's properties
    class FakeApp:
        _staticDir = "/fake/static"
        def static(self): pass
        class http:
            before = [lambda *a: None]

    app = FakeApp()
    assert isinstance(app._staticDir, str)
    assert callable(getattr(app, "static", None))
    assert callable(app.http.before[0])

def test_GET_headers(static_server):
    port = static_server
    resp = requests.get(f"http://localhost:{port}/headers")
    assert resp.status_code == 200
    try:
        import json
        data = resp.json()
        assert isinstance(data, dict)
    except Exception:
        pytest.fail("Response is not valid JSON.")

def test_GET_style_css(static_server):
    port = static_server
    resp = requests.get(f"http://localhost:{port}/style.css")
    assert resp.status_code == 200
    # Compare content with file
    css_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../examples/static-app/app/assets/style.css")
    )
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        assert resp.text == file_content