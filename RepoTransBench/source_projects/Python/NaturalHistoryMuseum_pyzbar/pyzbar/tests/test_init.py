import pyzbar

def test_version_exists():
    assert hasattr(pyzbar, '__version__')
    assert isinstance(pyzbar.__version__, str)