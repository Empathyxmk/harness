package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

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
		// Simulate injection on first attach
	} else {
		// Retained fragment; do not re-inject
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

func TestInjectingPreferenceFragment_OnAttach_FirstTime(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	assert.Nil(t, frag.GetObjectGraph())
	frag.OnAttach("Activity", "Module")
	assert.NotNil(t, frag.GetObjectGraph())
	assert.True(t, frag.firstAttach)
}

func TestInjectingPreferenceFragment_OnAttach_RetainedFragment(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", "Module")
	frag.OnAttach("Activity", "Module")
	assert.NotNil(t, frag.GetObjectGraph())
	assert.False(t, frag.firstAttach)
}

func TestInjectingPreferenceFragment_OnDestroy(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", "Module")
	assert.NotNil(t, frag.GetObjectGraph())
	frag.OnDestroy()
	assert.Nil(t, frag.GetObjectGraph())
}

func TestInjectingPreferenceFragment_GetObjectGraph(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", "Module")
	assert.NotNil(t, frag.GetObjectGraph())
}

func TestInjectingPreferenceFragment_Inject_GraphInitialized(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", "Module")
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic: %v", r)
		}
	}()
	frag.Inject(struct{}{})
}

func TestInjectingPreferenceFragment_Inject_GraphNotInitialized(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for uninitialized graph")
		}
	}()
	frag.Inject(struct{}{})
}

func TestInjectingPreferenceFragment_GetModules(t *testing.T) {
	frag := &InjectingPreferenceFragment{}
	frag.OnAttach("Activity", "Module")
	modules := frag.GetModules()
	assert.NotNil(t, modules)
	assert.Equal(t, 1, len(modules))
	assert.Equal(t, "Module", modules[0])
}