from rajinipp.runner import RppRunner

def test_public_runner_tokenize_and_exec(capsys):
    runner = RppRunner()
    code = 'print 1234;'
    runner.exec(code)
    out, err = capsys.readouterr()
    assert "1234" in out

def test_public_runner_eval_simple_line():
    runner = RppRunner()
    result = runner.eval("10 + 50")
    assert str(result) == "60.0" or str(result) == "60"