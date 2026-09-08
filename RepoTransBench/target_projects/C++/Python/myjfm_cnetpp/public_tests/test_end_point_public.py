import pytest

# Mock EndPoint
class EndPoint:
    def __init__(self):
        self._ip = ""
        self._port = 0

    def FromString(self, s):
        # Format: "IP:PORT"
        try:
            ip, port = s.split(":")
            self._ip = ip
            self._port = int(port)
            return True
        except Exception:
            return False

    def ToString(self):
        return f"{self._ip}:{self._port}"

    def port(self):
        return self._port

def test_set_get_ipv4():
    ep = EndPoint()
    assert ep.FromString("192.168.0.1:4321")
    assert ep.ToString() == "192.168.0.1:4321"
    assert ep.port() == 4321