package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Flow struct {
	State int
}

func NewFlow() *Flow {
	return &Flow{State: 2}
}

func (f *Flow) Run() int {
	return f.State * 3
}

func TestFlowPublicRun(t *testing.T) {
	flow := NewFlow()
	assert.Equal(t, 6, flow.Run())
}