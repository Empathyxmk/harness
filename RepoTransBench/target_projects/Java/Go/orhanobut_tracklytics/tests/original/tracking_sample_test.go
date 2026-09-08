package original

import (
	"testing"
)

type Event struct {
	Name string
}

type DummyEventSubscriber struct {
	triggeredEvents map[string]Event
}

func (des *DummyEventSubscriber) OnEventTracked(event Event) {
	des.triggeredEvents[event.Name] = event
}

type Foo struct{}
func (Foo) TrackFoo() Event {
	return Event{Name: "event_java"}
}

type FooKotlin struct{}
func (FooKotlin) TrackFoo() Event {
	return Event{Name: "event_kotlin"}
}

func TestConfirmKotlinAspects(t *testing.T) {
	es := &DummyEventSubscriber{triggeredEvents: make(map[string]Event)}
	event := FooKotlin{}.TrackFoo()
	es.OnEventTracked(event)
	if _, ok := es.triggeredEvents["event_kotlin"]; !ok {
		t.Fatalf("event_kotlin not in triggeredEvents map")
	}
}
func TestConfirmJavaAspects(t *testing.T) {
	es := &DummyEventSubscriber{triggeredEvents: make(map[string]Event)}
	event := Foo{}.TrackFoo()
	es.OnEventTracked(event)
	if _, ok := es.triggeredEvents["event_java"]; !ok {
		t.Fatalf("event_java not in triggeredEvents map")
	}
}