def test_hello(capsys):
    print("Hello world!")
    # Verify output string
    captured = capsys.readouterr()
    assert "Hello world!" in captured.out