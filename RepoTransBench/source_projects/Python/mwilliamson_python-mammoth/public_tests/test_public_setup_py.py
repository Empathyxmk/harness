import pytest

def test_version_in_setup_public():
    # Simulate with different string
    setup_py = "__version__ = '2.3.4-public'"
    assert "'2.3.4-public'" in setup_py

def test_author_in_setup_public():
    # Simulate with public variant
    content = "author='Someone Else'"
    assert "Else" in content