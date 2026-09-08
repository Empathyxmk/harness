package tests

import (
	"errors"
	"testing"
)

type EventPayloadSchemaRegistry struct {
	store map[interface{}]interface{}
}

func NewEventPayloadSchemaRegistry() *EventPayloadSchemaRegistry {
	return &EventPayloadSchemaRegistry{store: make(map[interface{}]interface{})}
}
func (r *EventPayloadSchemaRegistry) Register(eventName interface{}, val interface{}) {
	if eventName == nil {
		panic(errors.New("MissingEventNameDuringRegistration"))
	}
	r.store[eventName] = val
}
func (r *EventPayloadSchemaRegistry) Get(eventName interface{}) (interface{}, bool) {
	x, ok := r.store[eventName]
	return x, ok
}
func (r *EventPayloadSchemaRegistry) Len() int {
	return len(r.store)
}

func TestSchemaRegistrationWithExplicitEventName(t *testing.T) {
	type UserEvents string
	const SignedUp UserEvents = "USER_SIGNED_UP"
	type DummySchema struct{ username string }

	for _, eventName := range []interface{}{SignedUp, "USER_SIGNED_UP"} {
		registry := NewEventPayloadSchemaRegistry()
		registry.Register(eventName, DummySchema{})
		got, ok := registry.Get(eventName)
		if !ok {
			t.Fatalf("schema not found for event: %v", eventName)
		}
		if _, ok := got.(DummySchema); !ok {
			t.Errorf("expected DummySchema for registry[%v]", eventName)
		}
	}
}

func TestSchemaRegistrationWithEventNameFromSchema(t *testing.T) {
	type DummySchema struct {
		username     string
		eventNameStr string
	}
	registry := NewEventPayloadSchemaRegistry()
	schema := DummySchema{"", "USER_SIGNED_UP"}
	registry.Register(schema.eventNameStr, schema)
	got, ok := registry.Get(schema.eventNameStr)
	if !ok {
		t.Fatalf("schema not found for event: %v", schema.eventNameStr)
	}
	if _, ok := got.(DummySchema); !ok {
		t.Errorf("expected DummySchema for registry[%v]", schema.eventNameStr)
	}
}

func TestSchemaRegistrationWithoutEventName(t *testing.T) {
	registry := NewEventPayloadSchemaRegistry()
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for MissingEventNameDuringRegistration, got no panic")
		}
	}()
	registry.Register(nil, struct{}{})
	if registry.Len() != 0 {
		t.Errorf("expected registry empty because registration failed")
	}
}