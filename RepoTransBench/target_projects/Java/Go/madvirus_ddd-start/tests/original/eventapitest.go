package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Event struct {
	EventType string
	Source    string
}

type EventApi struct{}

func (api *EventApi) GetEvents(eventType string) []Event {
	if eventType == "OrderCreated" {
		return []Event{
			{EventType: "OrderCreated", Source: "system"},
		}
	}
	return []Event{}
}

func TestEventApiReturnsOrderCreated(t *testing.T) {
	api := &EventApi{}
	events := api.GetEvents("OrderCreated")
	assert.Len(t, events, 1)
	assert.Equal(t, "OrderCreated", events[0].EventType)
}

func TestEventApiReturnsEmptyForUnknownType(t *testing.T) {
	api := &EventApi{}
	events := api.GetEvents("UnknownType")
	assert.Len(t, events, 0)
}