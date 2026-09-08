def test_public_dynamic_properties(capsys):
    d = {}
    d["abc"] = 555
    d["def"] = "dynamicTest"
    d["ghi"] = d["abc"] + 20
    print(f"{d['abc']}, {d['def']}, {d['ghi']}")
    captured = capsys.readouterr()
    assert "555, dynamicTest, 575" in captured.out