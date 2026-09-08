import pytest

class MockMouse:
    def __init__(self, x=0, y=0):
        self._pos = [x, y]
        self._movements = []
    def getMousePosition(self):
        from collections import namedtuple
        Point = namedtuple('Point', ['x', 'y'])
        return Point(self._pos[0], self._pos[1])
    def mouseMove(self, x, y):
        self._pos = [x, y]
        from collections import namedtuple
        Point = namedtuple('Point', ['x', 'y'])
        self._movements.append(Point(x, y))
    def getMouseMovements(self):
        return self._movements.copy()

class MouseMotionTestBase:
    SMALL_DELTA = 1e-6
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    # Subclasses must set up these objects: factory, systemCalls, deviationProvider, noiseProvider, speedManager, random, mouse

    def setup_base(self):
        # Each test class must override and fully complete setup
        raise NotImplementedError()

    def assertMousePosition(self, x, y):
        pos = self.mouse.getMousePosition()
        assert abs(pos.x - x) < self.SMALL_DELTA
        assert abs(pos.y - y) < self.SMALL_DELTA