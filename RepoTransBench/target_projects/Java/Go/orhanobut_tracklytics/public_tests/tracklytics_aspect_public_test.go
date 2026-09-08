package public_tests

import (
	"testing"
)

type TrackEvent struct {
	Value    string
	Filters  []int
	Tags     []string
}

type AspectListener struct {
	OnAspectEventTriggeredFunc    func(te TrackEvent, attrs map[string]interface{})
	OnAspectSuperAttributeAdded   func(key string, value interface{})
	OnAspectSuperAttributeRemoved func(key string)
}

type TracklyticsAspect struct {
	listener *AspectListener
	trackEvent TrackEvent
	attributes map[string]interface{}
	superAttributes map[string]interface{}
}

func (t *TracklyticsAspect) Subscribe(al *AspectListener) {
	t.listener = al
}

func (t *TracklyticsAspect) WeaveJoinPointTrackEvent(eventName string, attrs map[string]interface{}) {
	ev := TrackEvent{Value: eventName}
	t.trackEvent = ev
	t.attributes = attrs
	if t.listener != nil && t.listener.OnAspectEventTriggeredFunc != nil {
		t.listener.OnAspectEventTriggeredFunc(ev, attrs)
	}
}

func TestTrackEventWithoutAttributesPublic(t *testing.T) {
	aspect := &TracklyticsAspect{}
	al := &AspectListener{}
	aspect.Subscribe(al)
	aspect.WeaveJoinPointTrackEvent("public_title", map[string]interface{}{})
	if aspect.trackEvent.Value != "public_title" {
		t.Fatalf("Expected event value 'public_title', got %s", aspect.trackEvent.Value)
	}
	if aspect.attributes == nil || len(aspect.attributes) != 0 {
		t.Fatalf("Expected no attributes, got %v", aspect.attributes)
	}
}