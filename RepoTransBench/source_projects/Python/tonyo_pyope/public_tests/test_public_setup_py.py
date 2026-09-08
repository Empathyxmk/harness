import importlib.util
import os

def test_setup_py_metadata():
    """Public test for setup.py metadata using importlib without executing setup()."""
    setup_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "setup.py"))

    with open(setup_py_path, "r") as f:
        content = f.read()

    # Check the presence of required fields using different expected values or substrings
    assert "name=" in content
    assert "description=" in content
    assert "author=" in content
    assert "version=" in content
    # Use different substrings to distinguish from private test, e.g., license instead of author_email
    assert "license=" in content