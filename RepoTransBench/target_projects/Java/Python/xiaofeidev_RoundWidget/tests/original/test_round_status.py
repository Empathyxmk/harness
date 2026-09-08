import pytest

class RoundStatus:
    def setRadius(self, value): pass
    def setTopLeftRadius(self, value): pass
    def setTopRightRadius(self, value): pass
    def setBottomLeftRadius(self, value): pass
    def setBottomRightRadius(self, value): pass
    def fillRadius(self): pass
    def getBottomLeftRadius(self): pass
    def getBottomRightRadius(self): pass
    def getRadius(self): pass
    def getRadiusList(self): pass
    def getTopRightRadius(self): pass
    def getTopLeftRadius(self): pass

class RoundStatusImpl(RoundStatus):
    def __init__(self):
        self._radius = 0.0
        self._top_left = 0.0
        self._top_right = 0.0
        self._bottom_left = 0.0
        self._bottom_right = 0.0
        self._radius_list = [0.0] * 8

    def setRadius(self, value):
        self._radius = value

    def setTopLeftRadius(self, value):
        self._top_left = value

    def setTopRightRadius(self, value):
        self._top_right = value

    def setBottomLeftRadius(self, value):
        self._bottom_left = value

    def setBottomRightRadius(self, value):
        self._bottom_right = value

    def fillRadius(self): pass

    def getBottomLeftRadius(self):
        return self._bottom_left

    def getBottomRightRadius(self):
        return self._bottom_right

    def getRadius(self):
        return self._radius

    def getRadiusList(self):
        return self._radius_list

    def getTopRightRadius(self):
        return self._top_right

    def getTopLeftRadius(self):
        return self._top_left

def test_interface_is_implemented():
    obj = RoundStatusImpl()
    obj.setRadius(7.2)
    obj.setTopLeftRadius(2.2)
    obj.setTopRightRadius(3.2)
    obj.setBottomLeftRadius(4.2)
    obj.setBottomRightRadius(5.2)

    obj.fillRadius()
    obj.getBottomLeftRadius()
    obj.getBottomRightRadius()
    obj.getRadius()
    obj.getRadiusList()
    obj.getTopRightRadius()
    obj.getTopLeftRadius()