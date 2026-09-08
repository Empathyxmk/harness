package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type LoggingManager struct{}

type ObjectGraph struct {
}

func (g *ObjectGraph) Inject(target interface{}) {}

type InjectingActionBarActivity struct {
	objectGraph *ObjectGraph
	modules     []interface{}
	created     bool
}

func (a *InjectingActionBarActivity) OnCreate(modules ...interface{}) {
	a.objectGraph = &ObjectGraph{}
	a.modules = modules
	a.created = true
}

func (a *InjectingActionBarActivity) OnDestroy() {
	a.objectGraph = nil
	a.created = false
}

func (a *InjectingActionBarActivity) GetObjectGraph() *ObjectGraph {
	return a.objectGraph
}

func (a *InjectingActionBarActivity) Inject(target interface{}) {
	if a.objectGraph == nil {
		panic("IllegalStateException")
	}
	a.objectGraph.Inject(target)
}

func (a *InjectingActionBarActivity) GetModules() []interface{} {
	return a.modules
}

func TestOnCreatePublic(t *testing.T) {
	act := &InjectingActionBarActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	assert.Nil(t, nil)
	assert.NotNil(t, act.GetObjectGraph())
	assert.ElementsMatch(t, modules, act.GetModules())
}

func TestOnDestroyPublic(t *testing.T) {
	act := &InjectingActionBarActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	assert.NotNil(t, act.GetObjectGraph())
	act.OnDestroy()
	assert.Nil(t, act.GetObjectGraph())
}

func TestGetObjectGraphPublic(t *testing.T) {
	act := &InjectingActionBarActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	assert.Equal(t, act.objectGraph, act.GetObjectGraph())
}

func TestInject_graphInitializedPublic(t *testing.T) {
	act := &InjectingActionBarActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic: %v", r)
		}
	}()
	act.Inject("SomeTarget")
}

func TestInject_graphNotInitializedPublic(t *testing.T) {
	act := &InjectingActionBarActivity{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for uninitialized graph")
		}
	}()
	act.Inject(123456)
}

func TestGetModulesPublic(t *testing.T) {
	act := &InjectingActionBarActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	ret := act.GetModules()
	assert.NotNil(t, ret)
	assert.Equal(t, 2, len(ret))
	_, ok0 := ret[0].(*InjectingActivityModule)
	_, ok1 := ret[1].(*LoggingManager)
	assert.True(t, ok0)
	assert.True(t, ok1)
}