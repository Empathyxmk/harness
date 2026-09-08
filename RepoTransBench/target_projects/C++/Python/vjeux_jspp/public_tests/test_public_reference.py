def test_public_reference_var_props(capsys):
    base = {"name": "root"}
    ref = base
    ref["name"] = "leaf"
    print(f"{base['name']}, {ref['name']}")
    captured = capsys.readouterr()
    # Both must be 'leaf'
    assert "leaf, leaf" in captured.out.strip()