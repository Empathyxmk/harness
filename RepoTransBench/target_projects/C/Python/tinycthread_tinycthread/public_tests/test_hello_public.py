def test_hello_public(capsys):
    print("Hello world!")  # The public test message
    # Verify output string
    captured = capsys.readouterr()
    assert "Hello world!" in captured.out