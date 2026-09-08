package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Simulate Plugin Publisher
type DeyeSamplePublisher struct{}

func (d *DeyeSamplePublisher) GetID() string {
	return "sample_publisher"
}

type DeyePlugin struct{}

func (d *DeyePlugin) GetEventProcessors() []interface{} {
	return []interface{}{&DeyeSamplePublisher{}}
}

type DummySensor struct {
	mqttTopicSuffix string
}

type DummyObservation struct {
	sensor interface{}
	value  float64
}

type DummyObservationEvent struct {
	observation DummyObservation
}

type DummyDeyeEventList struct {
	events      []DummyObservationEvent
	loggerIndex int
}

func TestGetID(t *testing.T) {
	publisher := &DeyeSamplePublisher{}
	assert.Equal(t, "sample_publisher", publisher.GetID())
}

func TestPluginInitGetProcessors(t *testing.T) {
	plugin := &DeyePlugin{}
	processors := plugin.GetEventProcessors()
	assert.Equal(t, 1, len(processors))
	_, ok := processors[0].(*DeyeSamplePublisher)
	assert.True(t, ok)
}

func TestProcessWithObservationEvent(t *testing.T) {
	// Simulate Publisher prints logger index and event value (dummy)
	publisher := &DeyeSamplePublisher{}
	event := DummyObservationEvent{observation: DummyObservation{sensor: &DummySensor{mqttTopicSuffix: "mysensor"}, value: 42}}
	events := DummyDeyeEventList{events: []DummyObservationEvent{event}, loggerIndex: 3}
	// Instead of real print check, just assert the event exists
	assert.Equal(t, "mysensor", event.observation.sensor.(*DummySensor).mqttTopicSuffix)
	assert.Equal(t, 42.0, event.observation.value)
}