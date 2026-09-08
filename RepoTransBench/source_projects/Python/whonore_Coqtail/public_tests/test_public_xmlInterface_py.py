import sys
import os

PYTHON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../python"))
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

import pytest

try:
    import xmlInterface
except ImportError:
    pytest.skip("xmlInterface.py not found", allow_module_level=True)

def has_function(obj, fn):
    return hasattr(obj, fn) and callable(getattr(obj, fn))

def test_public_escape_xml_symbol():
    if not has_function(xmlInterface, "escape"):
        pytest.skip("No escape function in xmlInterface")
    # Test escaping with additional symbols, not just < and >
    result = xmlInterface.escape("apples & bananas < oranges > \"g\"")
    assert "&amp;" in result and "&lt;" in result and "&gt;" in result and "&quot;" in result

def test_public_unescape_xml_symbol():
    if not has_function(xmlInterface, "unescape"):
        pytest.skip("No unescape function in xmlInterface")
    # Test that unescape can handle multiple XML escapes in string
    s = '&amp;hello&gt;&lt;test&gt;&quot;x&quot;'
    result = xmlInterface.unescape(s)
    assert "&" in result and ">" in result and "<" in result and '"' in result

def test_public_make_elem_with_attrs():
    if not has_function(xmlInterface, "elem"):
        pytest.skip("No elem function in xmlInterface")
    # Use tag and content, with attributes as dictionary
    elem = xmlInterface.elem("fruit", "banana & apple", {"ripe": "yes", "color": "yellow"})
    assert "fruit" in elem and "ripe" in elem and "&amp;" in elem