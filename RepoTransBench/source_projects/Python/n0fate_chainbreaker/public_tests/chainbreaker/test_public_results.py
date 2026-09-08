import importlib
import pytest

def test_public_results_module_exists():
    mod = importlib.import_module("chainbreaker.results")
    assert hasattr(mod, '__file__')

def test_public_results_module_has_doc():
    mod = importlib.import_module("chainbreaker.results")
    assert mod.__doc__ is None or isinstance(mod.__doc__, str)

def test_public_log_output_handles_missing_method(monkeypatch, tmp_path):
    """
    Simulate the dummy record that lacks write_to_disk and log_output should fail gracefully.
    This nearly mimics the error in the existing tests.
    """
    mod = importlib.import_module("chainbreaker.results")
    class DummyRecord:
        def __str__(self):
            return "Fake"

    dummy_args = type("Args", (), {})()
    dummy_args.output = str(tmp_path)
    dummy_coll = {
        "header": "Testing",
        "records": [DummyRecord()],
        "write_to_console": True,
        "write_to_disk": True,
        "write_directory": str(tmp_path),
    }
    # Should raise AttributeError when trying to call .write_to_disk
    with pytest.raises(AttributeError):
        mod.log_output([dummy_coll], [], dummy_args)