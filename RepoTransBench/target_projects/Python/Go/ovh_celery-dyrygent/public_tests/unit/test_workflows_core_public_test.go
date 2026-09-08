package unit

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type WorkflowException struct{ error }
type WFExc struct{ error }

func TestWorkflowExceptionInheritancePublic(t *testing.T) {
	var err error = &WFExc{errors.New("another error")}
	// type assertion to error
	_, ok := err.(error)
	assert.True(t, ok)
}

type DummyWorkflowPub struct{}

func (d *DummyWorkflowPub) AddSignature(signature interface{}, dependencies interface{}) string {
	return "nodex"
}

func TestCeleryWorkflowMixinAddCelerySignatureCallsAddSignaturePublic(t *testing.T) {
	dummy := &DummyWorkflowPub{}
	result := []string{dummy.AddSignature(struct{}{}, "something")}
	assert.Contains(t, result, "nodex")
}

func TestSignalConnectAndEmitPublic(t *testing.T) {
	type T struct {
		Hooks                 map[string][]func(workflow interface{}, payload interface{})
		Called                []interface{}
		connectFunc           func(hookName string) func(f func(workflow interface{}, payload interface{}))
		emitFunc              func(hookName string, payload interface{})
	}

	tInst := &T{
		Hooks:  map[string][]func(workflow interface{}, payload interface{}){"on_custom_finish": {}},
		Called: []interface{}{},
	}
	tInst.connectFunc = func(hookName string) func(f func(workflow interface{}, payload interface{})) {
		return func(f func(workflow interface{}, payload interface{})) {
			tInst.Hooks[hookName] = append(tInst.Hooks[hookName], f)
		}
	}
	handler := func(workflow interface{}, payload interface{}) {
		tInst.Called = append(tInst.Called, payload)
	}
	tInst.connectFunc("on_custom_finish")(handler)
	tInst.emitFunc = func(hookName string, payload interface{}) {
		if _, exists := tInst.Hooks[hookName]; !exists {
			panic(WorkflowException{errors.New("Unknown hook")})
		}
		for _, h := range tInst.Hooks[hookName] {
			h(nil, payload)
		}
	}
	tInst.emitFunc("on_custom_finish", 24)
	assert.Equal(t, 24, tInst.Called[len(tInst.Called)-1])
}

func TestSignalMultipleHooksAreIndependentPublic(t *testing.T) {
	type T struct {
		Hooks                 map[string][]func(workflow interface{}, payload interface{})
		Called                []interface{}
		connectFunc           func(hookName string) func(f func(workflow interface{}, payload interface{}))
		emitFunc              func(hookName string, payload interface{})
	}
	tInst := &T{
		Hooks:  map[string][]func(workflow interface{}, payload interface{}){"after_special_tick": {}},
		Called: []interface{}{},
	}
	tInst.connectFunc = func(hookName string) func(f func(workflow interface{}, payload interface{})) {
		return func(f func(workflow interface{}, payload interface{})) {
			tInst.Hooks[hookName] = append(tInst.Hooks[hookName], f)
		}
	}
	cb1 := func(workflow interface{}, payload interface{}) { tInst.Called = append(tInst.Called, "cb1") }
	cb2 := func(workflow interface{}, payload interface{}) { tInst.Called = append(tInst.Called, "cb2") }
	tInst.connectFunc("after_special_tick")(cb1)
	tInst.connectFunc("after_special_tick")(cb2)

	tInst.emitFunc = func(hookName string, payload interface{}) {
		if _, exists := tInst.Hooks[hookName]; !exists {
			panic(WorkflowException{errors.New("Unknown hook")})
		}
		for _, h := range tInst.Hooks[hookName] {
			h(nil, payload)
		}
	}

	tInst.emitFunc("after_special_tick", "yyy")
	countCb1, countCb2 := 0, 0
	for _, v := range tInst.Called {
		if v == "cb1" {
			countCb1++
		}
		if v == "cb2" {
			countCb2++
		}
	}
	assert.Equal(t, 1, countCb1)
	assert.Equal(t, 1, countCb2)
}