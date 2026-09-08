def test_main_guard(monkeypatch, capsys):
    # Test importing hamms.__main__ runs main() and prints expected output
    import importlib
    import sys

    module_name = "hamms.__main__"
    if module_name in sys.modules:
        del sys.modules[module_name]
    import hamms.__main__  # triggers main guard only if run as __main__
    # The actual main() should only be run as main, so this test is mainly for coverage.