package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type LoggingManager struct{}

type ObjectGraph struct {
}

func (g *ObjectGraph) Inject(target interface{}) {}

type InjectingPreferenceFragment struct {
	objectGraph *ObjectGraph
	modules     []interface{}
	firstAttach bool
}

func (f *InjectingPreferenceFragment) OnAttach(activity interface{}, modules ...interface{}) {
	if f.objectGraph == nil {
		f.objectGraph = &ObjectGraph{}
		f.modules = modules
		f.firstAttach = true
	} else {
		f.firstAttach = false
	}
}

func (f *InjectingPreferenceFragment) OnDestroy() {
	f.objectGraph = nil
}

func (f *InjectingPreferenceFragment) GetObjectGraph() *ObjectGraph {
	return f.objectGraph
}

func (f *InjectingPreferenceFragment) Inject(target interface{}) {
	if f.objectGraph == nil {
		panic("IllegalStateException")
	}
	f.objectGraph.Inject(target)
}

func (f *InjectingPreferenceFragment) GetModules() []interface{} {
	return f.modules
}

func TestOnAttach_FirstTimePublic(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	assert.Nil(t, frag.GetObjectGraph())
	frag.OnAttach("Activity", &LoggingManager{})
	assert.NotNil(t, frag.GetObjectGraph())
	assert.True(t, frag.firstAttach)
}

func TestOnAttach_RetainedFragmentPublic(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", &LoggingManager{})
	frag.OnAttach("Activity", &LoggingManager{})
	assert.NotNil(t, frag.GetObjectGraph())
	assert.False(t, frag.firstAttach)
}

func TestOnDestroyPublic(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", &LoggingManager{})
	assert.NotNil(t, frag.GetObjectGraph())
	frag.OnDestroy()
	assert.Nil(t, frag.GetObjectGraph())
}

func TestGetObjectGraphPublic(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", &LoggingManager{})
	assert.NotNil(t, frag.GetObjectGraph())
}

func TestInject_graphInitializedPublic(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", &LoggingManager{})
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic: %v", r)
		}
	}()
	frag.Inject("MyInjectedTarget")
}

func TestInject_graphNotInitializedPublic(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for uninitialized graph")
		}
	}()
	frag.Inject(999)
}

func TestGetModulesPublic(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", &LoggingManager{})
	modules := frag.GetModules()
	assert.NotNil(t, modules)
	assert.Equal(t, 1, len(modules))
	_, ok := modules[0].(*LoggingManager)
	assert.True(t, ok)
}