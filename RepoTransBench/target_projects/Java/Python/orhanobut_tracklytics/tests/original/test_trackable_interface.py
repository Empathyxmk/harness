import pytest

class Trackable:
    def getTrackableAttributes(self):
        raise NotImplementedError()

class DummyTrackable(Trackable):
    def getTrackableAttributes(self):
        return {"key": "val"}

def test_trackable_method():
    t = DummyTrackable()
    attrs = t.getTrackableAttributes()
    assert len(attrs) == 1
    assert attrs["key"] == "val"