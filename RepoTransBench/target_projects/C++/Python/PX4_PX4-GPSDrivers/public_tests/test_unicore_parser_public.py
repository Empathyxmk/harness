import pytest

from src.unicore import UnicoreParser

def test_empty_public():
    str_input = "\n\t"
    unicore_parser = UnicoreParser()
    for c in str_input:
        result = unicore_parser.parseChar(c)
        assert result == UnicoreParser.Result.None_

def test_garbage_public():
    str_input = "#RANDOM,DATA"
    unicore_parser = UnicoreParser()
    for c in str_input:
        result = unicore_parser.parseChar(c)
        assert result == UnicoreParser.Result.None_

def test_too_long_public():
    str_input = (
        "#UNIHEADINGA,93,GPS,FIXED,5678,168052901,1,1,22,15;COMPUTED_SOL,"
        "INT_PHASE,1.1234,75.5555,10.3001,0.2005,0.8429,2.2929,\"123\","
        "33,22,23,19,5,03,3,fc,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,9876543210,9876543210,9876543210,9876543210,9876543210,"
        "9876543210,00000000"
    )
    unicore_parser = UnicoreParser()
    for c in str_input:
        result = unicore_parser.parseChar(c)
        assert result == UnicoreParser.Result.None_

def test_uniheadinga_wrong_crc_public():
    str_input = (
       "#UNIHEADINGA,93,GPS,FIXED,5678,168052901,1,1,22,15;COMPUTED_SOL,INT_PHASE,"
       "1.1234,75.5555,10.3001,0.2005,0.8429,2.2929,\"123\",33,22,23,19,5,03,3,fc*"
       "baaaaaad"
    )
    unicore_parser = UnicoreParser()
    for c in str_input:
        result = unicore_parser.parseChar(c)
        if result == UnicoreParser.Result.WrongCrc:
            return
    pytest.fail("Should have encountered WrongCrc result")