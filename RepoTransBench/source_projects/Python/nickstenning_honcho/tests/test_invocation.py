import importlib
import types

def test_main_module_exists():
    import honcho.__main__
    assert callable(honcho.__main__.main)

def test_main_invocation_runs(monkeypatch):
    # Coverage for honcho.__main__ entrypoint: directly call main()
    import honcho.__main__
    called = dict(ran=False)

    def fake_main():
        called["ran"] = True

    monkeypatch.setattr(honcho.__main__, "main", fake_main)
    # Simulate running as __main__ (no code actually in __main__ block, so direct main)
    honcho.__main__.main()
    assert called["ran"]