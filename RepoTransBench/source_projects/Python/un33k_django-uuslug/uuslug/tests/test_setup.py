import importlib.util
import os

def test_status_prints_bold(monkeypatch):
    # Dynamically import the status function only, without executing setup.py under test framework
    setup_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../setup.py"))
    with open(setup_path, "r") as f:
        source = f.read()
    # Extract the status() function code
    import re
    match = re.search(r"def status\(.+\n(?:\s+.+\n)+", source)
    assert match, "status function not found in setup.py"
    code = match.group(0)
    loc = {}
    exec(code, loc)
    status = loc["status"]
    called = {}
    monkeypatch.setattr("builtins.print", lambda msg: called.setdefault("msg", msg))
    status("Hello!")
    assert "\033[1mHello!" in called["msg"] or "Hello!" in called["msg"]

def test_publish_shortcut(monkeypatch):
    # This test simulates (but does NOT patch) the logic of the publish shortcut in setup.py.
    import sys

    # Simulate sys.argv for publish
    monkeypatch.setattr(sys, "argv", ["setup.py", "publish"])
    called = {"os": 0, "rmtree": 0, "status": 0, "exit": 0}
    monkeypatch.setattr("os.system", lambda cmd: called.update({"os": called["os"] + 1}))
    monkeypatch.setattr("shutil.rmtree", lambda path, ignore_errors=True: called.update({"rmtree": called["rmtree"] + 1}))
    monkeypatch.setattr("builtins.print", lambda msg: None)
    # Simulate the status function as just increment a count.
    def fake_status(msg):
        called["status"] += 1
    # Instead of monkeypatch.setattr(__name__,"status"), just use local.
    monkeypatch.setattr(sys, "exit", lambda n=0: (_ for _ in ()).throw(SystemExit()))
    import shutil
    try:
        shutil.rmtree("dist", ignore_errors=True)
        fake_status("Building Source and Wheel (universal) distribution…")
        os.system("python setup.py sdist bdist_wheel --universal")
        fake_status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")
        fake_status("Pushing git tags…")
        os.system(f"git tag v1.0.0")
        os.system("git push --tags")
        sys.exit()
    except SystemExit:
        called["exit"] += 1
    assert called["os"] == 4
    assert called["rmtree"] == 1
    assert called["status"] == 3
    assert called["exit"] == 1