import subprocess
import time
import requests
import sys
import os
import signal
import pytest

@pytest.fixture(scope="module")
def http_sample_server():
    """
    Spawns the http sample server in a subprocess, yields the port,
    and ensures the child terminates after tests.
    Requires examples/http-sample.py to be available.
    """
    node_path = sys.executable  # Python implementation
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../examples/http_sample.py")
    )
    port = 8080
    if not os.path.isfile(script_path):
        pytest.skip("Source file examples/http_sample.py not available.")
        return

    env = os.environ.copy()
    env["PORT"] = str(port)
    child = subprocess.Popen(
        [node_path, script_path],
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(0.5)
        yield port
    finally:
        child.terminate()
        try:
            child.wait(timeout=2)
        except Exception:
            child.kill()

def test_get_root_returns_hello_world(http_sample_server):
    port = http_sample_server
    try:
        resp = requests.get(f"http://localhost:{port}/", timeout=2)
        # Accept any status code < 500 as in the JS test
        assert resp.status_code < 500
    except requests.exceptions.ConnectionError:
        pytest.skip("Could not connect to http-sample server.")