import pytest

class TrackEvent:
    def value(self): return "dummy_event"
    def filters(self): return [1,2]
    def tags(self): return ["tag1", "tag2"]

class Event:
    def __init__(self, name, filters, tags, attributes, super_attributes):
        self.name = name
        self.filters = list(filters)
        self.tags = list(tags)
        self.attributes = dict(attributes)
        self.superAttributes = dict(super_attributes)
        self.super_attributes = dict(super_attributes)
    @staticmethod
    def getAllAttributesStatic(attrs, super_attrs):
        all_attrs = dict(attrs)
        all_attrs.update(super_attrs)
        return all_attrs
    def getAllAttributes(self):
        return Event.getAllAttributesStatic(self.attributes, self.super_attributes)

def test_constructor_with_fields():
    name = "test"
    filters = [1,2]
    tags = ["t1", "t2"]
    attrs = {"a": "b"}
    super_attrs = {"x": "y"}
    ev = Event(name, filters, tags, attrs, super_attrs)
    assert ev.name == name
    assert ev.filters == filters
    assert ev.tags == tags
    assert ev.attributes == attrs
    assert ev.superAttributes == super_attrs

def test_constructor_with_track_event():
    te = TrackEvent()
    attrs = {"c": 1}
    super_attrs = {}
    ev = Event(te.value(), te.filters(), te.tags(), attrs, super_attrs)
    assert ev.name == "dummy_event"
    assert ev.filters == [1,2]
    assert ev.tags == ["tag1", "tag2"]
    assert ev.attributes == attrs
    assert ev.superAttributes == super_attrs

def test_get_all_attributes_no_overlap():
    attrs = {"foo": "bar"}
    super_attrs = {"hello": "world"}
    ev = Event("n", [], [], attrs, super_attrs)
    all_ = ev.getAllAttributes()
    assert len(all_) == 2
    assert all_["foo"] == "bar"
    assert all_["hello"] == "world"

def test_get_all_attributes_super_overrides_normal():
    attrs = {"foo": "bar", "a": 1}
    super_attrs = {"foo": "baz"}
    ev = Event("n", [], [], attrs, super_attrs)
    all_ = ev.getAllAttributes()
    assert len(all_) == 2
    assert all_["foo"] == "baz"
    assert all_["a"] == 1

def test_empty_attributes():
    ev = Event("event", [], [], {}, {})
    all_ = ev.getAllAttributes()
    assert isinstance(all_, dict)
    assert len(all_) == 0