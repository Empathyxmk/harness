import pytest

class TrackEvent:
    def value(self): return "public_event"
    def filters(self): return [3, 4]
    def tags(self): return ["pub1", "pub2"]

class Event:
    def __init__(self, name, filters, tags, attributes, super_attributes):
        self.name = name
        self.filters = list(filters)
        self.tags = list(tags)
        self.attributes = dict(attributes)
        self.superAttributes = dict(super_attributes)
        self.super_attributes = dict(super_attributes)
    def getAllAttributes(self):
        all_attrs = dict(self.attributes)
        all_attrs.update(self.super_attributes)
        return all_attrs

def test_constructor_with_different_fields():
    name = "demo"
    filters = [10, 20]
    tags = ["alpha", "beta"]
    attrs = {"m": "n"}
    super_attrs = {"foo": "bar"}
    ev = Event(name, filters, tags, attrs, super_attrs)
    assert ev.name == name
    assert ev.filters == filters
    assert ev.tags == tags
    assert ev.attributes == attrs
    assert ev.superAttributes == super_attrs

def test_constructor_with_different_track_event():
    te = TrackEvent()
    attrs = {"x": 2}
    super_attrs = {"y": "z"}
    ev = Event(te.value(), te.filters(), te.tags(), attrs, super_attrs)
    assert ev.name == "public_event"
    assert ev.filters == [3,4]
    assert ev.tags == ["pub1", "pub2"]
    assert ev.attributes == attrs
    assert ev.superAttributes == super_attrs

def test_get_all_attributes_different_keys():
    attrs = {"jack": "jill"}
    super_attrs = {"tango": "fox"}
    ev = Event("n2", [], [], attrs, super_attrs)
    all_ = ev.getAllAttributes()
    assert len(all_) == 2
    assert all_["jack"] == "jill"
    assert all_["tango"] == "fox"

def test_get_all_attributes_super_overrides_different():
    attrs = {"theme": "dark", "score": 100}
    super_attrs = {"theme": "light"}
    ev = Event("n3", [], [], attrs, super_attrs)
    all_ = ev.getAllAttributes()
    assert len(all_) == 2
    assert all_["theme"] == "light"
    assert all_["score"] == 100

def test_empty_attributes_public():
    ev = Event("public_event", [], [], {}, {})
    all_ = ev.getAllAttributes()
    assert isinstance(all_, dict)
    assert len(all_) == 0