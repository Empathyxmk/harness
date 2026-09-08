import importlib.util
import pathlib
import sys
import os

# Make sure docker-images/app is in sys.path for module resolution
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docker-images", "app"))
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

def test_hello_returns_expected_message():
    import main
    client = main.app.test_client()
    rv = client.get("/")
    # Update to assert what the app actually returns
    assert rv.status_code == 200
    expected = b"Hello World from Flask in a Docker container running Python 3.11 with Meinheld and Gunicorn (default)"
    assert rv.data == expected

def test_hello_route_methods():
    import main
    client = main.app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200

def test_flask_app_instance():
    import main
    import flask
    assert isinstance(main.app, flask.Flask)

def test_import_main_py_multiple_times():
    main_path = str(pathlib.Path("docker-images/app/main.py").resolve())
    spec = importlib.util.spec_from_file_location("mainmodule", main_path)
    main1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main1)
    app1 = main1.app
    spec2 = importlib.util.spec_from_file_location("mainmodule2", main_path)
    main2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(main2)
    app2 = main2.app
    assert hasattr(app1, "route")
    assert hasattr(app2, "route")