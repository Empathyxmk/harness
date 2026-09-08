import pytest

# Simulate constants
XDP_ABORTED = 0
XDP_DROP = 1
XDP_PASS = 2
XDP_TX = 3
XDP_ACTION_MAX = XDP_TX + 1
XDP_ACTION_MAX_STRLEN = 11

xdp_action_names = [
    "XDP_ABORTED",
    "XDP_DROP",
    "XDP_PASS",
    "XDP_TX"
]

def action2str(action):
    if 0 <= action < XDP_ACTION_MAX:
        return xdp_action_names[action]
    return None

def parse_xdp_action(action_str):
    maxlen = XDP_ACTION_MAX_STRLEN
    action = -1
    for i in range(XDP_ACTION_MAX):
        if xdp_action_names[i][:maxlen] == action_str[:maxlen]:
            action = i
            break
    return int(action)

def test_action2str():
    assert action2str(XDP_ABORTED) == "XDP_ABORTED"
    assert action2str(XDP_DROP) == "XDP_DROP"
    assert action2str(XDP_PASS) == "XDP_PASS"
    assert action2str(XDP_TX) == "XDP_TX"
    assert action2str(-1) is None
    assert action2str(100) is None

def test_parse_xdp_action():
    assert parse_xdp_action("XDP_ABORTED") == XDP_ABORTED
    assert parse_xdp_action("XDP_DROP") == XDP_DROP
    assert parse_xdp_action("XDP_PASS") == XDP_PASS
    assert parse_xdp_action("XDP_TX") == XDP_TX
    assert parse_xdp_action("INVALID") == -1
    assert parse_xdp_action("XDP") == -1

def test_main_called(capsys):
    test_action2str()
    test_parse_xdp_action()
    print("bench01 tests passed")
    out = capsys.readouterr().out
    assert "bench01 tests passed" in out