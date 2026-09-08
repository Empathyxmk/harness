package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type ObjectGraph struct {
	mock.Mock
}

func (g *ObjectGraph) Plus(modules ...interface{}) *ObjectGraph {
	args := g.Called(modules)
	return args.Get(0).(*ObjectGraph)
}

func (g *ObjectGraph) Inject(target interface{}) {
	g.Called(target)
}

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

func TestInjectingActionBarActivity_OnCreate(t *testing.T) {
	act := &InjectingActionBarActivity{}
	act.OnCreate("Module")
	og := act.GetObjectGraph()
	assert.NotNil(t, og)
	assert.True(t, act.created)
}

func TestInjectingActionBarActivity_OnDestroy(t *testing.T) {
	act := &InjectingActionBarActivity{}
	act.OnCreate("Module")
	assert.NotNil(t, act.GetObjectGraph())
	act.OnDestroy()
	assert.Nil(t, act.GetObjectGraph())
	assert.False(t, act.created)
}

func TestInjectingActionBarActivity_GetObjectGraph(t *testing.T) {
	act := &InjectingActionBarActivity{}
	act.OnCreate("Module")
	assert.NotNil(t, act.GetObjectGraph())
}

func TestInjectingActionBarActivity_Inject_GraphInitialized(t *testing.T) {
	act := &InjectingActionBarActivity{}
	act.OnCreate("Module")
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic: %v", r)
		}
	}()
	act.Inject(struct{}{})
}

func TestInjectingActionBarActivity_Inject_GraphNotInitialized(t *testing.T) {
	act := &InjectingActionBarActivity{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for uninitialized graph")
		}
	}()
	act.Inject(struct{}{})
}

func TestInjectingActionBarActivity_GetModules(t *testing.T) {
	act := &InjectingActionBarActivity{}
	act.OnCreate("Module")
	modules := act.GetModules()
	assert.NotNil(t, modules)
	assert.Equal(t, 1, len(modules))
	assert.Equal(t, "Module", modules[0])
}