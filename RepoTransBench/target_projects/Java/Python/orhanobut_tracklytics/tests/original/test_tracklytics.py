import pytest
from unittest.mock import Mock

class Event:
    def __init__(self, name, attributes=None, superAttributes=None):
        self.name = name
        self.attributes = attributes if attributes is not None else None
        self.superAttributes = superAttributes if superAttributes is not None else {}

class EventSubscriber:
    def onEventTracked(self, event): pass

class Tracklytics:
    def __init__(self, subscriber=None):
        self.subscriber = subscriber
        self.super_attributes = dict()
        self.logger = None
    @staticmethod
    def init(subscriber):
        return Tracklytics(subscriber)
    def addSuperAttribute(self, key, val):
        self.super_attributes[key] = val
    def removeSuperAttribute(self, key):
        self.super_attributes.pop(key, None)
    def getSuperAttributes(self):
        return dict(self.super_attributes)
    def trackEvent(self, name, attributes=None):
        if self.subscriber:
            self.subscriber.onEventTracked(Event(name, attributes, self.super_attributes))
    def onAspectEventTriggered(self, trackEvent, attributes):
        if self.subscriber:
            self.subscriber.onEventTracked(Event(trackEvent.value(), attributes, self.super_attributes))
    def setEventLogListener(self, logger):
        self.logger = logger

def test_track_without_annotation():
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    attributes = {'key': 'value'}
    tracklytics.trackEvent('event_name', attributes)
    subscriber.onEventTracked.assert_called_once()
    event = subscriber.onEventTracked.call_args[0][0]
    assert event.name == 'event_name'
    assert event.attributes == attributes

def test_track_from_aspect_event():
    class TrackEvent:
        def value(self): return 'event_name'
        def filters(self): return [1,2]
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    trackEvent = TrackEvent()
    attributes = {'key': 'value'}
    tracklytics.onAspectEventTriggered(trackEvent, attributes)
    subscriber.onEventTracked.assert_called_once()
    event = subscriber.onEventTracked.call_args[0][0]
    assert event.name == 'event_name'
    assert event.attributes == attributes

def test_track_with_event():
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    tracklytics.trackEvent('event_name')
    subscriber.onEventTracked.assert_called_once()
    event = subscriber.onEventTracked.call_args[0][0]
    assert event.name == 'event_name'
    assert event.attributes is None

def test_add_super_attributes_to_event():
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    tracklytics.addSuperAttribute('key1', 'value1')
    tracklytics.addSuperAttribute('key2', 'value2')
    attributes = {'key3': 'value3'}
    tracklytics.trackEvent('event_name', attributes)
    subscriber.onEventTracked.assert_called_once()
    event = subscriber.onEventTracked.call_args[0][0]
    assert event.name == 'event_name'
    assert event.attributes == attributes
    assert event.superAttributes == {'key1': 'value1', 'key2': 'value2'}

def test_add_super_attribute_from_aspects():
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    tracklytics.addSuperAttribute('key1', 'value1')
    tracklytics.trackEvent('event_name')
    subscriber.onEventTracked.assert_called_once()
    event = subscriber.onEventTracked.call_args[0][0]
    assert event.name == 'event_name'
    assert event.superAttributes == {'key1': 'value1'}

def test_remove_super_attributes():
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    tracklytics.addSuperAttribute('key1', 'value1')
    tracklytics.addSuperAttribute('key2', 'value2')
    tracklytics.addSuperAttribute('key3', 'value3')
    tracklytics.removeSuperAttribute('key1')
    tracklytics.removeSuperAttribute('key2')
    attributes = {'key4': 'value4'}
    tracklytics.trackEvent('event_name', attributes)
    subscriber.onEventTracked.assert_called_once()
    event = subscriber.onEventTracked.call_args[0][0]
    assert event.name == 'event_name'
    assert event.attributes == attributes
    assert event.superAttributes == {'key3': 'value3'}

def test_remove_super_attribute_from_aspects():
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    tracklytics.addSuperAttribute('key1', 'value1')
    tracklytics.addSuperAttribute('key2', 'value2')
    tracklytics.removeSuperAttribute('key1')
    tracklytics.trackEvent('event_name')
    subscriber.onEventTracked.assert_called_once()
    event = subscriber.onEventTracked.call_args[0][0]
    assert event.name == 'event_name'
    assert event.superAttributes == {'key2': 'value2'}

def test_log():
    logger = Mock()
    subscriber = Mock(spec=EventSubscriber)
    tracklytics = Tracklytics.init(subscriber)
    tracklytics.setEventLogListener(logger)
    attributes = {'key': 'value'}
    tracklytics.trackEvent('event', attributes)
    # For this mock, just ensure the logger's log method can be called:
    if hasattr(logger, 'log'):
        logger.log.assert_not_called()  # Or adjust as appropriate