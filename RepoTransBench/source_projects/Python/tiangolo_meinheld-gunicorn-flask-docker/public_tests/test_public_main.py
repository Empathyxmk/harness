import importlib.util
import pathlib
import sys
import os

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docker-images", "app"))
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

def test_hello_returns_custom_message():
    import main
    client = main.app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    # The default message in main.py always includes the Python version;
    # here, check that it starts as expected but do not match entire message
    assert rv.data.startswith(b"Hello World from Flask in a Docker container running Python ")

def test_hello_route_status_code():
    import main
    client = main.app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200

def test_flask_app_type():
    import main
    import flask
    assert type(main.app) is flask.Flask

def test_import_main_py_distinct_apps():
    main_path = str(pathlib.Path("docker-images/app/main.py").resolve())
    spec1 = importlib.util.spec_from_file_location("mainmoduleX", main_path)
    main1 = importlib.util.module_from_spec(spec1)
    spec1.loader.exec_module(main1)
    app1 = main1.app
    spec2 = importlib.util.spec_from_file_location("mainmoduleY", main_path)
    main2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(main2)
    app2 = main2.app
    assert app1 is not app2
    assert hasattr(app1, "route")
    assert hasattr(app2, "route")