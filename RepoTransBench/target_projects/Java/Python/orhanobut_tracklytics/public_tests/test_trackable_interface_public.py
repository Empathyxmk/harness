import pytest

class Event: pass

class Trackable:
    def onTracked(self, event): pass

class Bar(Trackable):
    def onTracked(self, event): pass

def test_implements_trackable_public():
    bar = Bar()
    assert isinstance(bar, Trackable)

def test_on_tracked_method_present_public():
    assert hasattr(Bar, 'onTracked')