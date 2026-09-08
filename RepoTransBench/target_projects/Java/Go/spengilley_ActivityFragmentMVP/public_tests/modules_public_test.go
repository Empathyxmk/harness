package public_tests

import (
	"testing"
	"github.com/spengilley/activityfragmentmvp/tests/original"
)

func TestModules_ListNonNullDifferentAppInstance(t *testing.T) {
	testApp := &original.App{}
	modules := original.Modules{}.list(testApp)
	if modules == nil {
		t.Fatal("Expected Modules.list() to return a non-nil slice")
	}
	if len(modules) == 0 {
		t.Error("Expected Modules.list() to return a non-empty slice")
	}
	if _, ok := modules[0].(*original.AppModule); !ok {
		t.Errorf("Expected modules[0] to be of type *AppModule")
	}
}