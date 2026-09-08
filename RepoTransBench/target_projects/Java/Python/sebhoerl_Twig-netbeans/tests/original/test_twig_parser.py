import pytest

class TwigParserResult:
    pass

class TwigParser:
    def parse(self, snapshot, arg2, arg3):
        return TwigParserResult()
    def getResult(self, arg):
        return TwigParserResult()

def test_parse_get_result():
    parser = TwigParser()
    snapshot = None
    result = parser.parse(snapshot, None, None)
    assert result is not None
    assert isinstance(result, TwigParserResult)
    r1 = parser.getResult(None)
    assert r1 is not None
    assert isinstance(r1, TwigParserResult)