def test_imports_public():
    # Just checks import works -- keep logic, change nothing
    import audiogrep
    assert hasattr(audiogrep, "__file__") or hasattr(audiogrep, "__doc__")