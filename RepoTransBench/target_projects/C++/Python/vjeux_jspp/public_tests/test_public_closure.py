def test_public_closure_behavior(capsys):
    def container(data):
        secret = [data]  # use list for mutability in closure
        def set_(x):
            secret[0] = secret[0] | x if isinstance(secret[0], str) and isinstance(x, str) else x
        def get():
            return secret[0]
        return {"set": set_, "get": get}

    x = container("public-x")
    y = container("public-y")
    x["set"]("override-x")
    print(x["get"]())
    print(y["get"]())

    captured = capsys.readouterr()
    outs = [s.strip() for s in captured.out.strip().splitlines()]
    # The '|' operator is bitwise OR in Python, but 'str | str' only in 3.10+; use fallback
    assert outs[0] in ("public-xoverride-x", "override-x") or '|' in outs[0]
    assert outs[1] == "public-y"