import pytest

# Simulated logic from src/is_procnet.c
def is_procnet(path):
    if not path:
        return 0
    if "/proc/net/" in path:
        return 1
    return 0

def test_procnet_tcp():
    assert is_procnet("/proc/net/tcp") == 1

def test_procnet_udp():
    assert is_procnet("/proc/net/udp") == 1

def test_not_procnet():
    assert is_procnet("/etc/passwd") == 0

def test_null_arg():
    assert is_procnet(None) == 0