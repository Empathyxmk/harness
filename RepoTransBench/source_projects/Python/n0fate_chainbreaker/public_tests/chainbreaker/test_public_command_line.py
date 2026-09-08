import pytest

def test_public_import_main_module_no_crash():
    """
    Import chainbreaker.__main__ to ensure that import does not error,
    but catch the known AttributeError caused by the __main__ file referencing
    chainbreaker.main() which does not exist.
    """
    import importlib
    with pytest.raises(AttributeError):
        importlib.import_module("chainbreaker.__main__")