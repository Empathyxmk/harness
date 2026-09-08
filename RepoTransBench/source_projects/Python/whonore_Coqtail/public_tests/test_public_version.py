import sys
import os

PYTHON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../python"))
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

try:
    import version
except ImportError:
    import pytest
    pytest.skip("version.py not found", allow_module_level=True)

def test_public_parse_version_minor():
    vstr = "Coq 8.15.0 (Feb 2022)"
    res = version.parse_version(vstr)
    assert isinstance(res, tuple)
    assert res[0] == 8 and res[1] == 15

def test_public_version_compare_greater_major():
    assert version.compare_version((8, 17, 0), (8, 16, 5)) > 0

def test_public_version_compare_smaller_minor():
    assert version.compare_version((8, 7, 1), (8, 8, 0)) < 0