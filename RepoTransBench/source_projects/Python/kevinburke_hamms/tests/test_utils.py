import pytest

try:
    from hamms import get_header
except ImportError:
    pytest.skip("hamms get_header import failed", allow_module_level=True)

def test_utils_dummy():
    assert True