def test_public_json_prints(capsys):
    obj = {"foo": 123, "baz": "testval", "arr": [2, 4, 6]}
    print(f"{obj['foo']}, {obj['baz']}, {obj['arr'][1]}")

    captured = capsys.readouterr()
    assert "123, testval, 4" in captured.out.strip()