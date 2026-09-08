import pytest
try:
    from src.parser import parser
except ImportError:
    parser = {}

def test_export_main_parsing_function():
    fn = None
    if callable(parser):
        fn = parser
    elif hasattr(parser, "parse"):
        fn = parser.parse
    elif hasattr(parser, "tokenize"):
        fn = parser.tokenize
    elif hasattr(parser, "parseLine"):
        fn = parser.parseLine
    assert callable(fn)