package public_tests

import (
	"testing"
	"github.com/spengilley/activityfragmentmvp/tests/original"
)

func TestApp_OnTerminateMultipleCalls(t *testing.T) {
	app := &original.App{}
	app.onTerminate()
	app.onTerminate()
	// No assertion: only coverage of multiple calls
}

func TestApp_BuildObjectGraphAndInjectMultipleTimes(t *testing.T) {
	app := &original.App{}
	app.buildObjectGraphAndInject()
	app.buildObjectGraphAndInject()
	if app.getApplicationGraph() == nil {
		t.Error("Expected application graph to be not nil after multiple buildObjectGraphAndInject calls")
	}
}

func TestApp_InjectWithStringObject(t *testing.T) {
	app := &original.App{}
	app.buildObjectGraphAndInject()
	someObj := "HelloPublic"
	app.inject(someObj)
	if app.getApplicationGraph() == nil {
		t.Error("Expected application graph to be not nil after inject of string")
	}
}

func TestApp_CreateScopedGraphWithLongerName(t *testing.T) {
	app := &original.App{}
	app.buildObjectGraphAndInject()
	scoped := app.createScopedGraph("publicModExtra")
	if scoped == nil {
		t.Error("Expected createScopedGraph with publicModExtra name to return non-nil graph")
	}
}