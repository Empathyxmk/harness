import pytest
from unittest.mock import Mock

class DummyAnimatorListener:
    def onAnimationStart(self, animator): pass
    def onAnimationEnd(self, animator): pass
    def onAnimationCancel(self, animator): pass
    def onAnimationRepeat(self, animator): pass

class DummyAnimatorSet:
    pass

class DummyView:
    pass

class DummyBaseAnimator:
    DURATION = 300

    def __init__(self):
        self._duration = self.DURATION
        self._animator_set = None
        self._listeners = []
        self._animated = False

    def setDuration(self, duration):
        self._duration = duration

    def getDuration(self):
        return self._duration

    def setAnimatorSet(self, animator_set):
        self._animator_set = animator_set

    def getAnimatorSet(self):
        return self._animator_set

    def addAnimatorListener(self, listener):
        self._listeners.append(listener)

    def animate(self, target):
        self.prepared = False
        self.prepare(target)
        self._animated = True

    def prepare(self, target):
        self.prepared = True

    def start(self):
        for listener in self._listeners:
            listener.onAnimationStart(self)
        # ... do some 'animation', then call end
        for listener in self._listeners:
            listener.onAnimationEnd(self)

def test_default_duration():
    animator = DummyBaseAnimator()
    assert animator.getDuration() == DummyBaseAnimator.DURATION

def test_set_animator_set():
    animator = DummyBaseAnimator()
    aset = DummyAnimatorSet()
    animator.setAnimatorSet(aset)
    assert animator.getAnimatorSet() is aset

def test_set_get_duration():
    animator = DummyBaseAnimator()
    animator.setDuration(500)
    assert animator.getDuration() == 500

def test_prepare_and_animate():
    animator = DummyBaseAnimator()
    dummy_view = DummyView()
    animator.prepared = False
    animator.animate(dummy_view)
    assert animator.prepared is True

def test_add_animator_listener_and_start(mocker):
    animator = DummyBaseAnimator()
    listener = Mock(spec=DummyAnimatorListener)
    animator.addAnimatorListener(listener)
    animator.start()
    listener.onAnimationStart.assert_called_once_with(animator)
    listener.onAnimationEnd.assert_called_once_with(animator)