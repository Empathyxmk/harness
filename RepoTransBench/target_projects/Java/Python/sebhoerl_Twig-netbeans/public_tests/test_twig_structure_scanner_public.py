import pytest

class TwigStructureScanner:
    def scan(self, input_str, arg):
        return []
    def getHeader(self, input_str):
        return None

def test_scan_empty_returns_list_public():
    scanner = TwigStructureScanner()
    assert scanner.scan("", None) == []

def test_get_header_returns_null_public():
    scanner = TwigStructureScanner()
    assert scanner.getHeader("") is None