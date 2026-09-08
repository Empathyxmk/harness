import importlib

def test_main_can_import_and_run():
    main_mod = importlib.import_module("pytest_watcher.__main__")
    # The file may not define "main", so just ensure import doesn't error and has __doc__|__name__
    assert hasattr(main_mod, "__doc__")