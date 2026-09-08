def test_public_operators_math(capsys):
    a = 8
    b = 17
    c = a * b + 2  # 8*17+2=138
    d = c // a - 3 # 138//8=17, 17-3=14
    print(f"a={a}")
    print(f"b={b}")
    print(f"c={c}")
    print(f"d={d}")
    if a == 8 and b == 17 and c == 138 and d == 14:
        print("Operator public test passed!")
        res = True
    else:
        print("Operator public test failed!")
        res = False
    captured = capsys.readouterr()
    assert "Operator public test passed!" in captured.out
    assert res is True