package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Mock types for demonstration (replace with your real implementation).
type Flow struct {
	State int
}

func NewFlow() *Flow {
	return &Flow{State: 1}
}

func (f *Flow) Run() int {
	return f.State * 2
}

func (f *Flow) Update(state int) {
	f.State = state
}

func TestFlowRun(t *testing.T) {
	flow := NewFlow()
	assert.Equal(t, 2, flow.Run())
	flow.Update(10)
	assert.Equal(t, 20, flow.Run())
}

func TestFlowInitialState(t *testing.T) {
	flow := NewFlow()
	assert.Equal(t, 1, flow.State)
}