import pytest

def test_basic_hello(capsys):
    # Public variant: echo different message
    print("Hi, public world!")
    captured = capsys.readouterr()
    assert "public world" in captured.out