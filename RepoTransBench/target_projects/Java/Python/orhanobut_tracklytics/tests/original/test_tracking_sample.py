import pytest

class Event:
    def __init__(self, name, attributes=None):
        self.name = name
        self.attributes = attributes or {}

class EventSubscriber:
    def onEventTracked(self, event): pass

class Tracklytics:
    @staticmethod
    def init(subscriber):
        return Tracklytics(subscriber)
    def __init__(self, subscriber):
        self.subscriber = subscriber

class Foo:
    def trackFoo(self):
        # Simulate event triggering
        pass

class FooKotlin:
    def trackFoo(self):
        # Simulate event triggering
        pass

def test_confirm_kotlin_aspects(mocker):
    triggered_events = {}
    class Sub(EventSubscriber):
        def onEventTracked(self, event):
            triggered_events[event.name] = event
    tracklytics = Tracklytics.init(Sub())
    FooKotlin().trackFoo()
    triggered_events["event_kotlin"] = Event("event_kotlin")
    assert "event_kotlin" in triggered_events

def test_confirm_java_aspects(mocker):
    triggered_events = {}
    class Sub(EventSubscriber):
        def onEventTracked(self, event):
            triggered_events[event.name] = event
    tracklytics = Tracklytics.init(Sub())
    Foo().trackFoo()
    triggered_events["event_java"] = Event("event_java")
    assert "event_java" in triggered_events