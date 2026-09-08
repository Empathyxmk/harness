def test_public_object_properties(capsys):
    o = {"fruit": "banana", "count": 4}
    print(f"{o['fruit']} ({o['count']})")

    captured = capsys.readouterr()
    assert "banana (4)" in captured.out