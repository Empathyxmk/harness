from rajinipp import rpp

def test_public_if_statement_true_branch(capsys):
    code = '''
    val x = 6
    if (x % 2 == 0) {
        print "even-case!";
    }
    '''
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "even-case!" in out

def test_public_while_loop_print(capsys):
    code = '''
    val count = 0
    while (count < 2) {
        print "loop: " + count;
        count = count + 1;
    }
    '''
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "loop: 0" in out
    assert "loop: 1" in out