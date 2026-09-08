package component

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type WorkflowSignalMixin struct {
	hooks        map[string][]func(interface{}, interface{})
}

func (m *WorkflowSignalMixin) Connect(hook string) func(cb func(interface{}, interface{})) {
	return func(cb func(interface{}, interface{})) {
		if m.hooks == nil {
			m.hooks = make(map[string][]func(interface{}, interface{}))
		}
		if _, ok := m.hooks[hook]; !ok {
			panic("invalid signal")
		}
		m.hooks[hook] = append(m.hooks[hook], cb)
	}
}

func (m *WorkflowSignalMixin) Emit(hook string, payload interface{}) {
	if m.hooks == nil || m.hooks[hook] == nil {
		panic("assertion error")
	}
	for _, cb := range m.hooks[hook] {
		cb(m, payload)
	}
}

func TestConnectAndEmitPublic(t *testing.T) {
	w := &WorkflowSignalMixin{hooks: map[string][]func(interface{}, interface{}){"on_custom": {}}}
	called := []int{}
	w.Connect("on_custom")(func(wf interface{}, payload interface{}) {
		called = append(called, payload.(int))
	})
	w.Emit("on_custom", 1001)
	assert.Equal(t, 1001, called[len(called)-1])
}

func TestConnectWrongHookPublic(t *testing.T) {
	w := &WorkflowSignalMixin{hooks: map[string][]func(interface{}, interface{}){}}
	assert.Panics(t, func() {
		w.Connect("unknown_hook")(nil)
	})
}

func TestEmitAssertionErrorPublic(t *testing.T) {
	w := &WorkflowSignalMixin{hooks: map[string][]func(interface{}, interface{}){"some_hook": {}}}
	assert.Panics(t, func() {
		w.Emit("unregistered_hook", "data")
	})
}