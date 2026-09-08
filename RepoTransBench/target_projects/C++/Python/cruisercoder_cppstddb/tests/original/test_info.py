from cppstddb import info

def test_one_arg(capsys):
    info("Test1")
    captured = capsys.readouterr()
    assert "Test1" in captured.out

def test_two_args(capsys):
    info("Test", 2)
    captured = capsys.readouterr()
    assert "Test2" in captured.out

def test_three_args(capsys):
    info("T", "WO", "RK")
    captured = capsys.readouterr()
    assert "TWORK" in captured.out