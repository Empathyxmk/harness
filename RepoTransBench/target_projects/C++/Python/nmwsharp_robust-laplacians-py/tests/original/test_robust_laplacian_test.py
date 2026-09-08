def test_import_core_from_package():
    from src.robust_laplacian import dummy_python_func
    assert callable(dummy_python_func)
    assert dummy_python_func(7) == 8