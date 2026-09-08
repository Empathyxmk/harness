def test_public_function_map_side_effect(capsys):
    def map_(array, func):
        for i in range(len(array)):
            array[i] = func(i, array[i])
    a = ["x", "y", "z"]
    print(a)
    map_(a, lambda key, value: f"[{key}|{value}]")
    print(a)

    captured = capsys.readouterr()
    outs = captured.out.strip().splitlines()
    assert outs[0] == "['x', 'y', 'z']"
    assert outs[1] == "['[0|x]', '[1|y]', '[2|z]']"