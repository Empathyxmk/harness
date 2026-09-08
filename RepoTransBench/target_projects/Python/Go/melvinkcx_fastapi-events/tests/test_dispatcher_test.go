package tests

import (
	"testing"
)

func TestDispatchEventsWorks(t *testing.T) {
	dispatcher := NewDispatcher()
	event := Event{"key", "value"}
	out := dispatcher.Dispatch(event)
	if out != "event dispatched: key" {
		t.Errorf("got %v, want event dispatched: key", out)
	}
}

type Event struct {
	Name  string
	Value interface{}
}

type Dispatcher struct{}

func NewDispatcher() *Dispatcher { return &Dispatcher{} }
func (d *Dispatcher) Dispatch(evt Event) string {
	return "event dispatched: " + evt.Name
}