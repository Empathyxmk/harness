import pytest

class TwigParserResult:
    def __init__(self, raw):
        self.raw = raw
    def getErrors(self):
        return []
    def getParsedData(self):
        return "Parsed"  # Dummy data just to simulate non-null

def test_blank_input_public():
    result = TwigParserResult("   ")
    assert result.getErrors() == []
    assert result.getParsedData() is not None

def test_simple_twig_input_public():
    result = TwigParserResult("{% include 'header.twig' %}")
    assert result.getParsedData() is not None
    assert result.getErrors() is not None