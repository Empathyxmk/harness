import sys
import types

def test_docs_conf_import(monkeypatch):
    called = {}
    class FakeSphinxMe:
        def setup_conf(self, g):
            called["ok"]=True
    sys.modules["sphinx_me"] = types.SimpleNamespace(setup_conf=lambda g: called.update({"run": True}))
    # execute code from docs/conf.py
    conf_path = __import__("os").path.join(__import__("os").path.dirname(__file__), "../../docs/conf.py")
    with open(conf_path) as f:
        code = f.read()
        exec(code, {})
    assert called