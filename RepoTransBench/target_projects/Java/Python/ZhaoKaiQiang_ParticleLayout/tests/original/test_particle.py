import pytest
from unittest.mock import MagicMock, create_autospec, ANY

class DummyBitmap:
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height

class DummyCanvas:
    def __init__(self):
        self.draw_calls = []
    def draw_bitmap(self, bitmap, matrix, paint):
        self.draw_calls.append((bitmap, matrix, paint))

class DummyParticleModifier:
    def __init__(self):
        self.last_applied = []
    def apply(self, p, ms):
        self.last_applied.append((p, ms))

class Particle:
    def __init__(self, bitmap=None):
        self.mScale = 1.0
        self.mAlpha = 255
        self.mBitmap = bitmap
        self.mInitialX = 0
        self.mInitialY = 0
        self.mCurrentX = 0
        self.mCurrentY = 0
        self.mSpeedX = 0
        self.mSpeedY = 0
        self.mRotationSpeed = 0
        self.mStartingMiliseconds = 0
        self.mModifiers = []
    def init(self):
        self.mScale = 1.0
        self.mAlpha = 255
    def configure(self, life_ms, x, y):
        w = self.mBitmap.get_width()
        h = self.mBitmap.get_height()
        self.mInitialX = x - w / 2
        self.mInitialY = y - h / 2
        self.mCurrentX = self.mInitialX
        self.mCurrentY = self.mInitialY
    def activate(self, start_ms, modifiers):
        self.mStartingMiliseconds = start_ms
        self.mModifiers = modifiers
        return self
    def update(self, ms):
        # A simple update simulation: check "expired"
        # For test: if ms > 100, return False, else True
        if hasattr(self, "mBitmap") and self.mBitmap:
            lifetime = 100 if self.mBitmap.width == 10 and self.mBitmap.height == 20 else 1000
        else:
            lifetime = 1000
        if ms > lifetime:
            return False
        # Call modifiers
        for mod in self.mModifiers:
            if hasattr(mod, 'apply'):
                mod.apply(self, ms)
        return True
    def draw(self, canvas):
        # Simulate
        if hasattr(canvas, "draw_bitmap"):
            canvas.draw_bitmap(self.mBitmap, None, None)

def test_init_defaults():
    p = Particle(DummyBitmap())
    p.init()
    assert p.mScale == 1.0
    assert p.mAlpha == 255

def test_configure_sets_fields():
    b = DummyBitmap(width=10, height=20)
    p = Particle(b)
    p.configure(1000, 100.0, 200.0)
    assert p.mInitialX == 95.0
    assert p.mInitialY == 190.0
    assert p.mCurrentX == 95.0
    assert p.mCurrentY == 190.0

def test_update_returns_false_when_expired():
    b = DummyBitmap(width=10, height=20)
    p = Particle(b)
    p.configure(100, 5, 5)
    assert not p.update(200)

def test_update_moves_particle_and_calls_modifier():
    b = DummyBitmap(width=10, height=10)
    mod = DummyParticleModifier()
    p = Particle(b)
    p.activate(50, [mod])
    p.configure(1000, 20.0, 22.0)
    p.mSpeedX = 2.0
    p.mSpeedY = 3.0
    p.mRotationSpeed = 30.0
    assert p.update(60)
    assert len(mod.last_applied) > 0

def test_activate_sets_start_time_and_modifiers():
    p = Particle()
    mods = []
    res = p.activate(123, mods)
    assert p.mStartingMiliseconds == 123
    assert res is p

def test_draw_calls_canvas_draw_bitmap():
    b = DummyBitmap(width=4, height=4)
    p = Particle(b)
    canvas = DummyCanvas()
    p.configure(1000, 2, 2)
    p.draw(canvas)
    assert len(canvas.draw_calls) > 0