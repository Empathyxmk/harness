package unit

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type inspectType struct{}

var Inspect = &inspectType{}

func (i *inspectType) inspectCommand(args ...interface{}) map[string]int {
	return map[string]int{}
}

func (i *inspectType) queueLength(q string) int {
	m := i.inspectCommand()
	v, ok := m[q]
	if ok {
		return v
	}
	return 0
}

func TestQueueLengthReturnsIntType(t *testing.T) {
	Inspect.inspectCommand = func(args ...interface{}) map[string]int {
		return map[string]int{"other-queue": 5}
	}
	result := Inspect.queueLength("other-queue")
	assert.IsType(t, int(0), result)
	assert.Equal(t, 5, result)
}

func TestQueueLengthReturnsZeroForMissingQueue(t *testing.T) {
	Inspect.inspectCommand = func(args ...interface{}) map[string]int {
		return map[string]int{"sample-queue": 3}
	}
	result := Inspect.queueLength("unseen-queue")
	assert.Equal(t, 0, result)
}

func TestInspectCommandHandlesEmpty(t *testing.T) {
	Inspect.inspectCommand = func(args ...interface{}) map[string]int {
		return map[string]int{}
	}
	assert.Equal(t, 0, Inspect.queueLength("noqueue"))
}