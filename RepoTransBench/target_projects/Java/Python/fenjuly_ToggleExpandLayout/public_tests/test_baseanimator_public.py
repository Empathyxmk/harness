import pytest

class DummyBaseAnimator:
    DURATION = 300

    def __init__(self):
        self._duration = self.DURATION
        self._animator_set = None
        self.prepared = False

    def setDuration(self, value):
        self._duration = value

    def getDuration(self):
        return self._duration

    def setAnimatorSet(self, aset):
        self._animator_set = aset

    def getAnimatorSet(self):
        return self._animator_set

    def animate(self, target):
        self.prepared = False
        self.prepare(target)

    def prepare(self, target):
        self.prepared = True

def test_durations_are_different_public():
    animator = DummyBaseAnimator()
    assert animator.getDuration() == DummyBaseAnimator.DURATION
    animator.setDuration(456)
    assert animator.getDuration() == 456
    animator.setDuration(880)
    assert animator.getDuration() == 880

def test_animator_set_public():
    animator = DummyBaseAnimator()
    newset = object()
    animator.setAnimatorSet(newset)
    assert animator.getAnimatorSet() is newset

def test_animate_prepares_public():
    animator = DummyBaseAnimator()
    target = object()
    assert animator.prepared is False
    animator.animate(target)
    assert animator.prepared is True