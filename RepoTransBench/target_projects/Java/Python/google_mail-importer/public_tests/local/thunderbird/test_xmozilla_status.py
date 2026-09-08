def parse_xmozilla_status(hex_string):
    return int(hex_string.lower().replace("0x", ""), 16)


def test_parses_different_hex_string():
    status = parse_xmozilla_status("0x0018")
    assert status == 0x18


def test_parses_different_hex_string_zero():
    status = parse_xmozilla_status("0x0")
    assert status == 0


def test_parses_different_hex_string_uppercase():
    status = parse_xmozilla_status("0X0022")
    assert status == 0x22