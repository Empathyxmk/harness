import pytest
from flask import Flask, jsonify
import threading
import requests

@pytest.fixture(scope="module")
def server():
    """
    Starts a Flask server for public test endpoints, auto-picking a port.
    Yields (base_url, thread, flask_app)
    """
    app = Flask(__name__)
    import socket

    @app.route("/sandwich/cheese")
    def sandwich_cheese():
        return jsonify({
            "sandwich": {
                "bread": True,
                "cheese": True,
                "bacon": False,
                "message": "Here is your cheese sandwich!"
            }
        })

    @app.route("/sandwich/lettuce")
    def sandwich_lettuce():
        return jsonify({"error": "lettuce sandwich not found"}), 404

    # Pick a random unused port
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()

    def run():
        app.run(port=port, use_reloader=False)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    import time
    time.sleep(0.5)  # Give time to start

    yield f"http://127.0.0.1:{port}"

    # Flask doesn't provide direct shutdown. In real code, send /shutdown or kill process.
    # This is sufficient for test fixture ending as thread is daemonized.

def test_get_sandwich_cheese(server):
    base_url = server
    resp = requests.get(f"{base_url}/sandwich/cheese")
    assert resp.status_code == 200
    data = resp.json()
    assert "sandwich" in data
    assert data["sandwich"]["cheese"] is True
    assert data["sandwich"]["bacon"] is False
    assert "cheese sandwich" in data["sandwich"]["message"].lower()

def test_get_sandwich_lettuce_not_found(server):
    base_url = server
    resp = requests.get(f"{base_url}/sandwich/lettuce")
    assert resp.status_code == 404
    data = resp.json()
    assert data.get("error") == "lettuce sandwich not found"