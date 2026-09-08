import pytest

try:
    from hamms import HammsServer, reactor
except ImportError:
    pytest.skip("hamms import failed", allow_module_level=True)

def test_dummy_server_start():
    assert True