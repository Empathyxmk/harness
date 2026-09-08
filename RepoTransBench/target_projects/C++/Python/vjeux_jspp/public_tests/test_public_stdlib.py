def test_public_stdlib_numbers_and_map(capsys):
    numbers = [8, 13, 21]
    info = {"alpha": 100, "beta": 200}

    print("Numbers: [{}]".format(", ".join(str(x) for x in numbers)))
    print("Info: {" + ", ".join(f"{k}: {v}" for k,v in info.items()) + "}")

    captured = capsys.readouterr()
    assert "Numbers: [8, 13, 21]" in captured.out
    assert "Info: {alpha: 100, beta: 200}" in captured.out