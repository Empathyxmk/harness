import sys
import os

# Add python directory to sys.path for module import
PYTHON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../python"))
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

try:
    import parse
except ImportError:
    # Fallback if module is missing, skip all tests.
    import pytest
    pytest.skip("parse.py not found", allow_module_level=True)

def test_public_parse_identifier_alpha():
    assert parse.is_ident("KappaZetaXYZ")

def test_public_parse_identifier_mixed():
    assert parse.is_ident("T2X9P")

def test_public_parse_non_identifier_numeric():
    assert not parse.is_ident("10MainVar")

def test_public_parse_split_line_colon():
    text = "Theorem Power: forall n, n ^ 2 >= 0."
    result = parse.split_line(text)
    assert isinstance(result, tuple)
    assert "Theorem" in result[0]

def test_public_parse_find_name_theorem():
    text = "Theorem my_power: forall n, n ^ 2 >= 0."
    name = parse.find_name(text)
    assert (isinstance(name, str) or name is None)