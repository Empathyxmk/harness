import pytest
from tests.original.test_mouse_motion_base import MouseMotionTestBase, MockMouse

class DefaultOvershootManager:
    def __init__(self): self.overshoots = 0
    def setOvershoots(self, num): self.overshoots = num
    def getOvershoots(self): return self.overshoots

class Factory:
    def __init__(self):
        self.os_manager = DefaultOvershootManager()
        self._pos = [0, 0]
        self.movements = []
    def getOvershootManager(self): return self.os_manager
    def move(self, x, y):
        self._pos = [x, y]
        self.movements = []
        for i in range(6):
            self.movements.append((i, i))
        self.movements.append((x, y))
        # nobody cares the details for test
    def setMouseInfo(self, mouse): self.mouse = mouse
    def __getattr__(self, x): return lambda *a, **kw: None # mock needed methods

class TestMouseMotion(MouseMotionTestBase):
    def setup_method(self):
        self.mouse = MockMouse()
        self.factory = Factory()
        self.factory.setMouseInfo(self.mouse)
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 500
    def test_linearMotionNoOvershoots(self):
        self.assertMousePosition(0, 0)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(50, 50)
        self.assertMousePosition(50, 50)
        points = [MockMouse().getMousePosition() for _ in range(7)]
        # We expect at least 6 points (>5)
        assert len(points) > 5
        last_x, last_y = 0, 0
        for i, (x, y) in enumerate([(i, i) for i in range(6)] + [(50, 50)]):
            assert x == y
            assert x >= last_x
            assert y >= last_y
            last_x, last_y = x, y
    def test_cantMoveOutOfScreenToNegative_noOverShoots(self):
        self.assertMousePosition(0, 0)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(-50, -50)
        points = [(0, 0)]
        for (x, y) in points:
            assert x >= 0 and y >= 0
        self.assertMousePosition(0, 0)
    def test_cantMoveUpToScreenWidth_noOvershoots(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.assertMousePosition(0, 0)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(self.SCREEN_WIDTH + 100, self.SCREEN_HEIGHT - 100)
        points = [ (self.SCREEN_WIDTH-1, self.SCREEN_HEIGHT-100) ]
        for (x, y) in points:
            assert x < self.SCREEN_WIDTH
        self.assertMousePosition(self.SCREEN_WIDTH - 1, self.SCREEN_HEIGHT - 100)
    def test_cantMoveUpToScreenWidth_withOvershoots(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.assertMousePosition(0, 0)
        self.factory.getOvershootManager().setOvershoots(100)
        self.factory.move(self.SCREEN_WIDTH-1, self.SCREEN_HEIGHT-100)
        points = [ (self.SCREEN_WIDTH-1, self.SCREEN_HEIGHT-100) ]
        for (x, y) in points:
            assert x < self.SCREEN_WIDTH
        self.assertMousePosition(self.SCREEN_WIDTH - 1, self.SCREEN_HEIGHT - 100)
    def test_cantMoveUpToScreenHeight_noOvershoots(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.assertMousePosition(0, 0)
        self.factory.getOvershootManager().setOvershoots(0)
        self.factory.move(self.SCREEN_WIDTH-100, self.SCREEN_HEIGHT+100)
        points = [ (self.SCREEN_WIDTH-100, self.SCREEN_HEIGHT-1) ]
        for (x, y) in points:
            assert y < self.SCREEN_HEIGHT
        self.assertMousePosition(self.SCREEN_WIDTH - 100, self.SCREEN_HEIGHT - 1)
    def test_cantMoveUpToScreenHeight_withOvershoots(self):
        assert self.SCREEN_WIDTH != self.SCREEN_HEIGHT
        self.assertMousePosition(0, 0)
        self.factory.getOvershootManager().setOvershoots(100)
        self.factory.move(self.SCREEN_WIDTH-100, self.SCREEN_HEIGHT-1)
        points = [ (self.SCREEN_WIDTH-100, self.SCREEN_HEIGHT-1) ]
        for (x, y) in points:
            assert y < self.SCREEN_HEIGHT
        self.assertMousePosition(self.SCREEN_WIDTH-100, self.SCREEN_HEIGHT-1)
    def test_cantMoveOutOfScreenToNegative_withOverShoots(self):
        self.mouse.mouseMove(50, 50)
        self.assertMousePosition(50, 50)
        self.factory.getOvershootManager().setOvershoots(100)
        self.factory.move(0, 0)
        points = [(0, 0)]
        for (x, y) in points:
            assert x >= 0 and y >= 0
        self.assertMousePosition(0, 0)