import pytest
from unittest.mock import MagicMock

# Simulated class
class ParkingBasicDataSync:
    def accept(self, request):
        try:
            body = request.getParameter("jsonBody")
        except Exception:
            return "fail"
        if body is not None:
            return "success"
        else:
            return "fail"

def test_accept_returns_success():
    sync = ParkingBasicDataSync()
    req = MagicMock()
    req.getParameter.return_value = '{"key":"value"}'
    ret = sync.accept(req)
    assert "success" in ret

def test_accept_returns_fail():
    sync = ParkingBasicDataSync()
    req = MagicMock()
    req.getParameter.return_value = None
    ret = sync.accept(req)
    assert "fail" in ret

def test_accept_exception_in_parameter():
    sync = ParkingBasicDataSync()
    req = MagicMock()
    req.getParameter.side_effect = RuntimeError("error")
    ret = sync.accept(req)
    assert "fail" in ret