import pytest

try:
    from hamms import morse
except ImportError:
    pytest.skip("hamms.morse import failed", allow_module_level=True)

def test_morse_dummy():
    assert True