from rajinipp import rpp

def test_public_function_different_content(capsys):
    # Use a different function that prints a different message
    code = """
    function greet() {
      print "Public Test Hello!";
    }
    greet()
    """
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "Public Test Hello!" in out

def test_public_function_return_different_value(capsys):
    # Function returning a different float value
    code = """
    function add(a, b) {
      return a + b;
    }
    val result = add(75, 125)
    print "Public Test - Result: " + result;
    """
    rpp.exec(code)
    out, err = capsys.readouterr()
    assert "Public Test - Result: 200" in out or "Public Test - Result: 200.0" in out