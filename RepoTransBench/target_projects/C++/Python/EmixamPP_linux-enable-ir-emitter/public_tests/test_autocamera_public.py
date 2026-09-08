import pytest

class AutoCamera:
    def __init__(self):
        self._exposure = 0
        self._focus = 0

    def setExposure(self, value):
        self._exposure = int(value)

    def getExposure(self):
        return self._exposure

    def setFocus(self, value):
        self._focus = int(value)

    def getFocus(self):
        return self._focus

def test_set_and_get_exposure():
    cam = AutoCamera()
    # Use a different exposure from private tests
    cam.setExposure(750)
    assert cam.getExposure() == 750
    cam.setExposure(0) # Minimum edge case
    assert cam.getExposure() == 0

def test_set_and_get_focus():
    cam = AutoCamera()
    # Use a different focus value from private tests
    cam.setFocus(1234)
    assert cam.getFocus() == 1234
    cam.setFocus(9876) # Another value
    assert cam.getFocus() == 9876

def test_multiple_settings():
    cam = AutoCamera()
    cam.setExposure(500)
    cam.setFocus(1111)
    # Setting both and then verifying
    assert cam.getExposure() == 500
    assert cam.getFocus() == 1111