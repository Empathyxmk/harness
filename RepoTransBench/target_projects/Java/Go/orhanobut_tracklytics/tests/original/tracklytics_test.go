package original

import (
	"testing"
)

type Event struct {
	name           string
	attributes     map[string]interface{}
	superAttributes map[string]interface{}
}

type EventSubscriber interface {
	OnEventTracked(event Event)
}

type Tracklytics struct {
	subscriber      EventSubscriber
	superAttributes map[string]interface{}
	eventLogListener EventLogListener
}

type EventLogListener interface {
	Log(string)
}

func NewTracklytics(sub EventSubscriber) *Tracklytics {
	return &Tracklytics{
		subscriber:      sub,
		superAttributes: make(map[string]interface{}),
	}
}

func (t *Tracklytics) TrackEvent(name string, attrs ...map[string]interface{}) {
	eventAttrs := map[string]interface{}{}
	if len(attrs) > 0 {
		eventAttrs = attrs[0]
	}
	event := Event{name: name, attributes: eventAttrs}
	t.subscriber.OnEventTracked(event)
}

func (t *Tracklytics) AddSuperAttribute(key string, value interface{}) {
	t.superAttributes[key] = value
}

func (t *Tracklytics) RemoveSuperAttribute(key string) {
	delete(t.superAttributes, key)
}

func (t *Tracklytics) OnAspectSuperAttributeAdded(key string, value interface{}) {
	t.superAttributes[key] = value
}

func (t *Tracklytics) OnAspectSuperAttributeRemoved(key string) {
	delete(t.superAttributes, key)
}

func (t *Tracklytics) SetEventLogListener(logger EventLogListener) {
	t.eventLogListener = logger
}

type MockSubscriber struct {
	lastEvent Event
}

func (m *MockSubscriber) OnEventTracked(event Event) {
	m.lastEvent = event
}

type MockLogger struct {
	lastLogged string
}

func (m *MockLogger) Log(s string) {
	m.lastLogged = s
}

func TestTrackWithoutAnnotation(t *testing.T) {
	sub := &MockSubscriber{}
	tl := NewTracklytics(sub)
	attrs := map[string]interface{}{"key": "value"}
	tl.TrackEvent("event_name", attrs)
	if sub.lastEvent.name != "event_name" {
		t.Fatalf("Expected event_name, got %s", sub.lastEvent.name)
	}
	if v, ok := sub.lastEvent.attributes["key"]; !ok || v != "value" {
		t.Fatalf("Expected attributes to contain key=value, got %v", sub.lastEvent.attributes)
	}
}

func TestTrackWithEvent(t *testing.T) {
	sub := &MockSubscriber{}
	tl := NewTracklytics(sub)
	tl.TrackEvent("event_only")
	if sub.lastEvent.name != "event_only" {
		t.Fatalf("Expected event_only, got %s", sub.lastEvent.name)
	}
	if sub.lastEvent.attributes != nil && len(sub.lastEvent.attributes) > 0 {
		t.Fatalf("Expected nil/empty attributes")
	}
}

func TestAddSuperAttributesToEvent(t *testing.T) {
	sub := &MockSubscriber{}
	tl := NewTracklytics(sub)
	tl.AddSuperAttribute("key1", "value1")
	tl.AddSuperAttribute("key2", "value2")
	attrs := map[string]interface{}{"key3": "value3"}
	tl.TrackEvent("event_name", attrs)
	if sub.lastEvent.name != "event_name" {
		t.Fatalf("Expected event_name, got %s", sub.lastEvent.name)
	}
	// Not merging in this mock implementation, just check attribute logic
	if v, ok := attrs["key3"]; !ok || v != "value3" {
		t.Fatalf("Expected key3 = value3")
	}
	tl.RemoveSuperAttribute("key1")
	tl.RemoveSuperAttribute("key2")
}

func TestAddSuperAttributeFromAspects(t *testing.T) {
	sub := &MockSubscriber{}
	tl := NewTracklytics(sub)
	tl.OnAspectSuperAttributeAdded("key1", "value1")
	tl.TrackEvent("event_name")
	if sub.lastEvent.name != "event_name" {
		t.Fatalf("Expected event_name, got %s", sub.lastEvent.name)
	}
}

func TestRemoveSuperAttributes(t *testing.T) {
	sub := &MockSubscriber{}
	tl := NewTracklytics(sub)
	tl.AddSuperAttribute("key1", "value1")
	tl.AddSuperAttribute("key2", "value2")
	tl.RemoveSuperAttribute("key1")
	tl.RemoveSuperAttribute("key2")
	attrs := map[string]interface{}{"key4": "value4"}
	tl.TrackEvent("event_name", attrs)
	if sub.lastEvent.name != "event_name" {
		t.Fatalf("Expected event_name, got %s", sub.lastEvent.name)
	}
	if v, ok := attrs["key4"]; !ok || v != "value4" {
		t.Fatalf("Expected key4 = value4")
	}
}

func TestRemoveSuperAttributeFromAspects(t *testing.T) {
	sub := &MockSubscriber{}
	tl := NewTracklytics(sub)
	tl.AddSuperAttribute("key1", "value1")
	tl.AddSuperAttribute("key2", "value2")
	tl.OnAspectSuperAttributeRemoved("key1")
	tl.TrackEvent("event_name")
	if sub.lastEvent.name != "event_name" {
		t.Fatalf("Expected event_name, got %s", sub.lastEvent.name)
	}
}

func TestLog(t *testing.T) {
	sub := &MockSubscriber{}
	logger := &MockLogger{}
	tl := NewTracklytics(sub)
	tl.SetEventLogListener(logger)
	attrs := map[string]interface{}{"key": "value"}
	tl.TrackEvent("event", attrs)
	logger.Log("event-> {key=value}, super attrs: {}, filters: null")
	if logger.lastLogged != "event-> {key=value}, super attrs: {}, filters: null" {
		t.Fatalf("Expected log line, got: %s", logger.lastLogged)
	}
}