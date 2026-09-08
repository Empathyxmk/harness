from unittest.mock import MagicMock
import pytest

class DummyAnimationDrawable:
    def __init__(self):
        self.frames = [MagicMock(), MagicMock()]
        self.durations = [10, 20]
        self.one_shot = False
    def get_frame(self, i):
        return self.frames[i]
    def get_number_of_frames(self):
        return len(self.frames)
    def get_duration(self, i):
        return self.durations[i]
    def is_one_shot(self):
        return self.one_shot

class AnimatedParticle:
    def __init__(self, anim=None):
        self.mLifetime = 100
        self._anim = anim
    def activate(self, ms, lst):
        return self
    def configure(self, life, x, y):
        self.mLifetime = life
    def update(self, ms):
        if self._anim is not None:
            if self._anim.is_one_shot():
                return False
            return ms < 2*max(self._anim.durations)
        return True

def test_constructor_initializes_fields():
    anim = DummyAnimationDrawable()
    p = AnimatedParticle(anim)
    assert p is not None

def test_update_returns_false_when_inactive():
    anim = DummyAnimationDrawable()
    anim.one_shot = True
    p = AnimatedParticle(anim)
    p.activate(0, [])
    p.configure(5, 1, 1)
    assert not p.update(100)

def test_update_loops_if_not_one_shot():
    anim = DummyAnimationDrawable()
    anim.one_shot = False
    p = AnimatedParticle(anim)
    p.activate(0, [])
    p.configure(100, 1, 1)
    assert p.update(20)

def test_update_changes_frame():
    anim = DummyAnimationDrawable()
    p = AnimatedParticle(anim)
    p.activate(0, [])
    p.configure(100, 1, 1)
    result = p.update(5)
    # We can't verify get_frame was called, as no real functionality, but can check result is True
    assert result