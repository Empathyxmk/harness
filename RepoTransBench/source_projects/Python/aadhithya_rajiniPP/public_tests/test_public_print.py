from rajinipp import rpp

def test_public_print_simple_message(capsys):
    code = 'print "Public output!";'
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "Public output!" in out

def test_public_print_number_and_string_concat(capsys):
    code = 'val score = 99\nprint "Score: " + score;'
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "Score: 99" in out