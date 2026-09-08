def test_public_constructor_like_func(capsys):
    def Animal(type_):
        return {"type": type_, "says": "hello"}
    d = Animal("dog")
    print(f"{d['type']}, {d['says']}")
    captured = capsys.readouterr()
    assert "dog, hello" in captured.out