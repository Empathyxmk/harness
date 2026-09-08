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

class DefaultOvershootManager:
    def __init__(self):
        self.overshoots = 0
    def setOvershoots(self, n):
        self.overshoots = n
    def getOvershoots(self):
        return self.overshoots

class Factory:
    def __init__(self):
        self.os_manager = DefaultOvershootManager()
        self.mouse = MockMouse(10, 10)
        self.movements = []
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 500
    def getOvershootManager(self):
        return self.os_manager
    def setMouseInfo(self, mouse): self.mouse = mouse
    def move(self, x, y):
        # fudge a path
        x0, y0 = self.mouse._pos
        points = []
        for i in range(6):
            step_x = x0 + int((x - x0)*i/6)
            step_y = y0 + int((y - y0)*i/6)
            points.append((step_x, step_y))
        points.append((x, y))
        for p in points:
            self.mouse.mouseMove(*p)
    def __getattr__(self, k):
        return lambda *a, **kw: None

class TestMouseMotionPublic:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500

    def setup_method(self):
        self.mouse = MockMouse(10, 10)
        self.factory = Factory()
        self.factory.setMouseInfo(self.mouse)
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 500

    def assertMousePosition(self, x, y):
        pos = self.mouse.getMousePosition()
        assert pos.x == x
        assert pos.y == y

    def test_linearMotionNoOvershoots_public(self):
        self.assertMousePosition(10, 10)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(30, 80)
        self.assertMousePosition(30, 80)
        points = self.mouse.getMouseMovements()
        assert len(points) > 5, "Path too short; should be more movement points."
        lastPoint = (10, 10)
        for p in points:
            # (p.x-10)*7 == (p.y-10)*2 on a line
            assert (p.x - 10) * 7 == (p.y - 10) * 2
            assert p.x >= lastPoint[0]
            assert p.y >= lastPoint[1]
            lastPoint = (p.x, p.y)
    def test_cantMoveOutOfScreenToNegative_noOverShoots_public(self):
        self.mouse = MockMouse(2, 2)
        self.factory.setMouseInfo(self.mouse)
        self.assertMousePosition(2, 2)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(-150, -250)
        points = self.mouse.getMouseMovements()
        for p in points:
            assert p.x >= 0 and p.y >= 0
        self.assertMousePosition(0, 0)
    def test_cantMoveUpToScreenWidth_noOvershoots_public(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.assertMousePosition(0, 0)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(self.SCREEN_WIDTH + 120, self.SCREEN_HEIGHT // 2)
        self.assertMousePosition(self.SCREEN_WIDTH - 1, self.SCREEN_HEIGHT // 2)
    def test_cantMoveUpToScreenWidth_withOvershoots_public(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.mouse = MockMouse(2, 2)
        self.factory.setMouseInfo(self.mouse)
        self.assertMousePosition(2, 2)
        self.factory.getOvershootManager().setOvershoots(14)
        self.factory.move(self.SCREEN_WIDTH - 2, self.SCREEN_HEIGHT // 4)
        self.assertMousePosition(self.SCREEN_WIDTH - 2, self.SCREEN_HEIGHT // 4)
    def test_cantMoveUpToScreenHeight_noOvershoots_public(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.mouse = MockMouse(3, 3)
        self.factory.setMouseInfo(self.mouse)
        self.assertMousePosition(3, 3)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT + 73)
        self.assertMousePosition(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 1)
    def test_cantMoveUpToScreenHeight_withOvershoots_public(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.mouse = MockMouse(7, 7)
        self.factory.setMouseInfo(self.mouse)
        self.assertMousePosition(7, 7)
        self.factory.getOvershootManager().setOvershoots(13)
        self.factory.move(self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT - 2)
        self.assertMousePosition(self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT - 2)
    def test_cantMoveOutOfScreenToNegative_withOverShoots_public(self):
        self.mouse = MockMouse(70, 15)
        self.factory.setMouseInfo(self.mouse)
        self.assertMousePosition(70, 15)
        self.factory.getOvershootManager().setOvershoots(17)
        self.factory.move(0, 0)
        self.assertMousePosition(0, 0)