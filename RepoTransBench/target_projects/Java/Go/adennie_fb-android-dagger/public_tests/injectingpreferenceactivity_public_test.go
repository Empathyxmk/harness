package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type LoggingManager struct{}

type ObjectGraph struct {
}

func (g *ObjectGraph) Inject(target interface{}) {}

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

func TestOnCreatePublicPreference(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	assert.NotNil(t, act.GetObjectGraph())
	assert.True(t, act.created)
}

func TestOnDestroyPublicPreference(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	assert.NotNil(t, act.GetObjectGraph())
	act.OnDestroy()
	assert.Nil(t, act.GetObjectGraph())
	assert.False(t, act.created)
}

func TestGetObjectGraphPublicPreference(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	assert.NotNil(t, act.GetObjectGraph())
}

func TestInject_graphInitializedPublicPreference(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	modules := []interface{}{&InjectingActivityModule{}, &LoggingManager{}}
	act.OnCreate(modules...)
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic: %v", r)
		}
	}()
	act.Inject("AnotherTarget")
}

func TestInject_graphNotInitializedPublicPreference(t *testing.T) {
	act := &InjectingPreferenceActivity{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for uninitialized graph")
		}
	}()
	act.Inject(0.01)
}

func TestGetModulesPublicPreference(t *testing.T) {
	act := &InjectingPreferenceActivity{}
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