import pytest
from flask import Flask, jsonify

@pytest.fixture
def app(tmp_path):
    # Setup a temporary static folder for each test
    static_dir = tmp_path / 'static'
    static_dir.mkdir()
    (static_dir / "hello.txt").write_text("hello static world!")

    app = Flask(__name__, static_folder=str(static_dir))

    @app.route('/api')
    def api():
        return jsonify(success=True)

    @app.errorhandler(404)
    def not_found(e):
        return "Not Found", 404

    return app

def test_get_non_existent_path_returns_404(app):
    client = app.test_client()
    rv = client.get('/nonexistent')
    assert rv.status_code == 404
    assert b"Not Found" in rv.data

def test_get_api_returns_not_404(app):
    client = app.test_client()
    rv = client.get('/api')
    assert rv.status_code == 200
    assert rv.json["success"] is True

def test_static_file_serving_returns_200(app):
    client = app.test_client()
    rv = client.get('/static/hello.txt')
    assert rv.status_code == 200
    assert b"hello static world!" in rv.data

def test_static_file_serving_nonexistent_returns_404(app):
    client = app.test_client()
    rv = client.get('/static/not-here.txt')
    assert rv.status_code == 404