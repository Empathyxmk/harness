from src.inverter_cli.inverter import cInverter

def test_getter_and_setter_status():
    inv = cInverter("mockdev", 1, 2, 3, 4)
    # SetMode and GetMode
    assert inv.GetMode() == 0  # Unknown

    modes = [
        {'mode': 'P', 'expected': 1},
        {'mode': 'S', 'expected': 2},
        {'mode': 'L', 'expected': 3},
        {'mode': 'B', 'expected': 4},
        {'mode': 'F', 'expected': 5},
        {'mode': 'H', 'expected': 6},
        {'mode': 'Q', 'expected': 0}
    ]
    for m in modes:
        inv.SetMode(m['mode'])
        assert inv.GetMode() == m['expected']

    # Status/warning getters: as default, should return empty string
    s1 = inv.GetQpigsStatus()
    s2 = inv.GetQpiriStatus()
    ws = inv.GetWarnings()
    assert s1 == ""
    assert s2 == ""
    assert ws == ""