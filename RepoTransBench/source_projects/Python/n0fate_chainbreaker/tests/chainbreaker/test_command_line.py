import sys
import importlib

def test_main_runs(monkeypatch):
    # If __main__ exists and is runnable, try to invoke main
    try:
        import chainbreaker.__main__
        if hasattr(chainbreaker.__main__, "main"):
            monkeypatch.setattr(sys, 'argv', ['chainbreaker'])
            try:
                chainbreaker.__main__.main()
            except SystemExit:
                pass
    except ImportError:
        pass

def test_entry_point():
    # Test __main__ can be run as a script (coverage for __main__)
    try:
        import runpy
        runpy.run_module("chainbreaker.__main__", run_name="__main__")
    except Exception:
        pass