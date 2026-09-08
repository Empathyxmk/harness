from rajinipp import rpp

def test_public_simple_arithmetic_expr(capsys):
    code = "print 20 + 10 + 5;"
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "35" in out or "35.0" in out

def test_public_float_expr_result(capsys):
    code = "print 7.5 * 4;"
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "30" in out or "30.0" in out