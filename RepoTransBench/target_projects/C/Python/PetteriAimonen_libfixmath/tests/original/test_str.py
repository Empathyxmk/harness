from src.libfixmath_python.fix16 import fix16_to_str, fix16_from_str, fix16_from_dbl, fix16_maximum, fix16_minimum, fix16_one

def test_str_to():
    assert fix16_to_str(fix16_from_dbl(1234.5678), None, 4) == "1234.5678"
    assert fix16_to_str(fix16_from_dbl(-1234.5678), None, 4) == "-1234.5678"
    assert fix16_to_str(0, None, 0) == "0"
    assert fix16_to_str(fix16_from_dbl(0.9), None, 0) == "1"
    assert fix16_to_str(1, None, 5) == "0.00002"
    assert fix16_to_str(-1, None, 5) == "-0.00002"
    assert fix16_to_str(65535, None, 5) == "0.99998"
    assert fix16_to_str(65535, None, 4) == "1.0000"
    assert fix16_to_str(fix16_maximum, None, 5) == "32767.99998"
    assert fix16_to_str(fix16_minimum, None, 5) == "-32768.00000"

def test_str_from():
    assert fix16_from_str("1234.5678") == fix16_from_dbl(1234.5678)
    assert fix16_from_str("-1234.5678") == fix16_from_dbl(-1234.5678)
    assert fix16_from_str("   +1234,56780   ") == fix16_from_dbl(1234.5678)
    assert fix16_from_str("0") == 0
    assert fix16_from_str("1") == fix16_one
    assert fix16_from_str("1.0") == fix16_one
    assert fix16_from_str("1.0000000000") == fix16_one
    assert fix16_from_str("0.00002") == 1
    assert fix16_from_str("0.99998") == 65535
    assert fix16_from_str("32767.99998") == fix16_maximum
    assert fix16_from_str("-32768.00000") == fix16_minimum

def test_str_extended():
    from src.libfixmath_python.fix16 import fix16_to_dbl
    import math
    value = fix16_minimum
    while value < fix16_maximum:
        fvalue = fix16_to_dbl(value)
        fvalue = round(fvalue * 100000.) / 100000.
        goodbuf = "{:0.5f}".format(fvalue)
        testbuf = fix16_to_str(value, None, 5)
        assert goodbuf == testbuf
        roundtrip = fix16_from_str(testbuf)
        assert roundtrip == value
        value += 0x10001