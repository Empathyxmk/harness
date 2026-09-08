def test_public_exception_message(capsys):
    print("Error: New Exception!")
    captured = capsys.readouterr()
    assert "Error: New Exception!" in captured.out.strip()