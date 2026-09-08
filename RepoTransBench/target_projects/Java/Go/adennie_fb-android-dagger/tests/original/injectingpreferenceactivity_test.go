package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type InjectingPreferenceActivity struct {
	objectGraph *ObjectGraph
	modules     []interface{}
	created     bool
}

func (a *InjectingPreferenceActivity) OnCreate(modules ...interface{}) {
	a.objectGraph = &ObjectGraph{}
	a.modules = modules
	a.created = true
}

func (a *InjectingPreferenceActivity) OnDestroy() {
	a.objectGraph = nil
	a.created = false
}

func (a *InjectingPreferenceActivity) GetObjectGraph() *ObjectGraph {
	return a.objectGraph
}

func (a *InjectingPreferenceActivity) Inject(target interface{}) {
	if a.objectGraph == nil {
		panic("IllegalStateException")
	}
	a.objectGraph.Inject(target)
}

func (a *InjectingPreferenceActivity) GetModules() []interface{} {
	return a.modules
}

func TestInjectingPreferenceActivity_OnCreate(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	act.OnCreate("Module")
	og := act.GetObjectGraph()
	assert.NotNil(t, og)
	assert.True(t, act.created)
}

func TestInjectingPreferenceActivity_OnDestroy(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	act.OnCreate("Module")
	assert.NotNil(t, act.GetObjectGraph())
	act.OnDestroy()
	assert.Nil(t, act.GetObjectGraph())
	assert.False(t, act.created)
}

func TestInjectingPreferenceActivity_GetObjectGraph(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	act.OnCreate("Module")
	assert.NotNil(t, act.GetObjectGraph())
}

func TestInjectingPreferenceActivity_Inject_GraphInitialized(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	act.OnCreate("Module")
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic: %v", r)
		}
	}()
	act.Inject(struct{}{})
}

func TestInjectingPreferenceActivity_Inject_GraphNotInitialized(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for uninitialized graph")
		}
	}()
	act.Inject(struct{}{})
}

func TestInjectingPreferenceActivity_GetModules(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	act.OnCreate("Module")
	modules := act.GetModules()
	assert.NotNil(t, modules)
	assert.Equal(t, 1, len(modules))
	assert.Equal(t, "Module", modules[0])
}