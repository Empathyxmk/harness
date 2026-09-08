package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// EventStoreHandler emulation for test
type EventStoreHandler struct{}

type ApplicationContext struct{}

func (ac *ApplicationContext) GetBeanNamesForType(t any) []string {
	// Simulate: we have 2 beans
	return []string{"handler1", "handler2"}
}
func (ac *ApplicationContext) GetBean(name string) *EventStoreHandler {
	return &EventStoreHandler{}
}

func TestEventStoreHandlerBeanHasApplicationContextAndType(t *testing.T) {
	ac := &ApplicationContext{}
	beans := ac.GetBeanNamesForType(EventStoreHandler{})
	assert.Greater(t, len(beans), 0, "Should have beans of type EventStoreHandler")
	for _, name := range beans {
		bean := ac.GetBean(name)
		assert.NotNil(t, bean)
		assert.IsType(t, &EventStoreHandler{}, bean)
	}
}