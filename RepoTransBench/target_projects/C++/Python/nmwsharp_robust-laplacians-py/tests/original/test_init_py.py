def test_init_import_star():
    import src.robust_laplacian
    assert hasattr(src.robust_laplacian, "dummy_python_func")