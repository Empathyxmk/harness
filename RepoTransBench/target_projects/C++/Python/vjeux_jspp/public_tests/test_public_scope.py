def test_public_scope_var_naming(capsys):
    val = 88
    def foo():
        val_inner = 49
        return val_inner + 1
    print(val)
    print(foo())

    captured = capsys.readouterr()
    # First line should be 88, second should be 50
    outputs = [s.strip() for s in captured.out.strip().splitlines()]
    assert outputs[0] == '88'
    assert outputs[1] == '50'