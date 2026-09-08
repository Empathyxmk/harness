import http.client
import time
import threading
import socket

import pytest

def is_server_running(host, port, path="/"):
    # Try to connect to the server at host:port
    conn = None
    try:
        conn = http.client.HTTPConnection(host, port, timeout=2)
        conn.request("GET", path)
        response = conn.getresponse()
        status_code = response.status
        response.read()
        conn.close()
        return status_code
    except Exception:
        if conn:
            conn.close()
        return None

@pytest.fixture(scope="module", autouse=True)
def ensure_server():
    # Best-effort: Try to import app.py, give time for possible server start
    try:
        import importlib.util, sys, os
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app.py'))
        if os.path.isfile(file_path):
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                spec = importlib.util.spec_from_file_location("app", file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
    except Exception:
        pass
    time.sleep(0.5)  # Give some time for server to possibly start

def test_running_express_server_on_some_port():
    # Try to connect to localhost:3000
    status_code = is_server_running('localhost', 3000, '/')
    assert status_code is not None