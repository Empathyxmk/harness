import pytest

class Tracklytics:
    def __init__(self):
        self.super_attributes = {}

    def addSuperAttribute(self, key, value):
        self.super_attributes[key] = value

    def removeSuperAttribute(self, key):
        if key in self.super_attributes:
            del self.super_attributes[key]

    def getSuperAttributes(self):
        return dict(self.super_attributes)

class Event:
    def __init__(self, name, filters=None, tags=None, attributes=None, super_attributes=None):
        self.name = name
        self.filters = filters or []
        self.tags = tags or []
        self.attributes = attributes or {}
        self.superAttributes = super_attributes or {}
        self.super_attributes = super_attributes or {}

    def getAllAttributes(self):
        all_attrs = dict(self.attributes)
        all_attrs.update(self.super_attributes)
        return all_attrs

def test_add_and_remove_super_attribute_public():
    t = Tracklytics()
    t.addSuperAttribute("pubA", 42)
    assert t.getSuperAttributes()["pubA"] == 42
    t.removeSuperAttribute("pubA")
    assert "pubA" not in t.getSuperAttributes()

def test_track_event_with_super_attributes_public():
    t = Tracklytics()
    t.addSuperAttribute("pubX", 99)
    attrs = {"pubY": "fooBar"}
    event = Event("pEvent", filters=[8], tags=["pT"], attributes=attrs, super_attributes=t.getSuperAttributes())
    all_attrs = event.getAllAttributes()
    assert all_attrs["pubY"] == "fooBar"
    assert all_attrs["pubX"] == 99