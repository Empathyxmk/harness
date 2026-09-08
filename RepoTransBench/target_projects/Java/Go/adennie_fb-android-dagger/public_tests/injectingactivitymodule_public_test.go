package public_tests

import (
	"testing"
	"reflect"

	"github.com/stretchr/testify/assert"
	"adennie_fb-android-dagger/tests/testutil"
)

type DummyModule struct {
	Name string
}

type DummyActivity struct {
	Injected bool
}

func TestInjectingActivityModule_InjectsDependencies(t *testing.T) {
	module := &DummyModule{Name: "m1"}
	graph := testutil.NewMockObjectGraph()
	app := testutil.SetupInjectingApp(graph)

	activity := &DummyActivity{}
	// Simulate injection via ObjectGraph
	err := app.Injector.Inject(activity)
	assert.NoError(t, err)
	called := false
	for _, obj := range graph.InjectedObjects() {
		if obj == activity {
			called = true
		}
	}
	assert.True(t, called, "Inject should be called with the activity")
}

func TestInjectingActivityModule_ObjectGraphPlus(t *testing.T) {
	module1 := &DummyModule{Name: "m1"}
	module2 := &DummyModule{Name: "m2"}
	graph := testutil.NewMockObjectGraph()
	app := testutil.SetupInjectingApp(graph)

	// Simulate ObjectGraph.Plus
	plusGraph := graph.Plus(module1, module2)
	assert.NotNil(t, plusGraph)
	assert.True(t, reflect.DeepEqual(graph.Modules, []interface{}{module1, module2}), "Modules should be appended")
}