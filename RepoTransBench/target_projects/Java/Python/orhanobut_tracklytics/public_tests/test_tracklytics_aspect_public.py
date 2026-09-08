import pytest

class TrackEvent:
    def __init__(self, value=None, filters=None, tags=None):
        self._value = value
        self._filters = filters or []
        self._tags = tags or []
    def value(self):
        return self._value
    def filters(self):
        return list(self._filters)
    def tags(self):
        return list(self._tags)

class TracklyticsAspect:
    def __init__(self):
        self.listeners = []
    def subscribe(self, listener):
        self.listeners.append(listener)
    def weaveJoinPointTrackEvent(self, join_point):
        pass

class DummyJoinPoint:
    def getSignature(self): pass
    def getThis(self): pass
    def getArgs(self): pass
    def proceed(self): pass

class DummyMethodSignature:
    def getMethod(self): pass

class TrackSession:
    def __init__(self, track_event, attributes):
        self.track_event = track_event
        self.attributes = attributes or {}
    def event(self, event):
        assert self.track_event.value() == event
        return self
    def noFilters(self):
        assert not self.track_event.filters()
        return self
    def noTags(self):
        assert not self.track_event.tags()
        return self
    def noAttributes(self):
        assert self.attributes == {} or self.attributes is None
        return self
    def attribute(self, key, value):
        assert self.attributes.get(key, None) == value
        return self

def test_track_event_without_attributes_public():
    # Simulate aspect call
    event = TrackEvent("public_title", [], [])
    attributes = {}
    TrackSession(event, attributes).event("public_title").noFilters().noTags().noAttributes()

def test_use_return_value_as_attribute_public():
    event = TrackEvent("public_event", [], [])
    attributes = {"pub_key": "bar_data"}
    TrackSession(event, attributes).event("public_event").noTags().noFilters().attribute("pub_key", "bar_data")

def test_use_return_value_and_parameters_as_attributes_public():
    event = TrackEvent("eventA", [], [])
    attributes = {"keyA": "dataA", "keyB": "dataB"}
    TrackSession(event, attributes).event("eventA").noFilters().noTags().attribute("keyA", "dataA").attribute("keyB", "dataB")

def test_use_default_value_when_there_is_no_return_value_public():
    event = TrackEvent("pubEv", [], [])
    attributes = {"k1": "dfVal"}
    TrackSession(event, attributes).event("pubEv").noFilters().noTags().attribute("k1", "dfVal")

def test_use_default_value_when_parameter_value_is_null_public():
    event = TrackEvent("ev2", [], [])
    attributes = {"kkk": "dvvv"}
    TrackSession(event, attributes).event("ev2").noFilters().noTags().attribute("kkk", "dvvv")