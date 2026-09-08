from src.inverter_cli.inverter import cInverter

def test_status_and_mode_branches_with_different_values():
    inv = cInverter("mockdev_public", 10, 20, 30, 40)

    modes = [
        {'mode': 'S', 'expected': 2},
        {'mode': 'P', 'expected': 1},
        {'mode': 'F', 'expected': 5},
        {'mode': 'B', 'expected': 4},
        {'mode': 'H', 'expected': 6},
        {'mode': 'X', 'expected': 0},  # X should be unknown
        {'mode': 'L', 'expected': 3}
    ]
    assert inv.GetMode() == 0
    for m in modes:
        inv.SetMode(m['mode'])
        assert inv.GetMode() == m['expected']

    # Set status and warning strings; check return values
    inv.status1 = "QPiGS"
    inv.status2 = "QPiRI"
    inv.warnings = "WarnTest"
    assert inv.GetQpigsStatus() == "QPiGS"
    assert inv.GetQpiriStatus() == "QPiRI"
    assert inv.GetWarnings() == "WarnTest"