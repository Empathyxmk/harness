import pytest

# Simulate logic from src/hide_tcp_ports.c

def port_hidden(proc_tcp, port):
    if not proc_tcp or port <= 0:
        return -1
    if "HIDDEN" in proc_tcp and port == 31337:
        return 1
    return 0

def test_hidden_port():
    content = "HIDDEN"
    assert port_hidden(content, 31337) == 1

def test_nonhidden_port():
    content = "OPEN"
    assert port_hidden(content, 80) == 0

def test_invalid_args():
    assert port_hidden(None, 0) == -1