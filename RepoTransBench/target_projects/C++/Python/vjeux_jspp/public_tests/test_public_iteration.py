def test_public_iteration_different_values(capsys):
    items = ["x", "y", "z"]
    print("[" + ", ".join(items) + "]")
    print("[" + ", ".join(f"({i}:{v})" for i, v in enumerate(items)) + "]")

    captured = capsys.readouterr()
    outs = captured.out.strip().splitlines()
    assert outs[0] == "[x, y, z]"
    assert outs[1] == "[(0:x), (1:y), (2:z)]"