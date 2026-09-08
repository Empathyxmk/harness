package opensource

import (
	"testing"
)

func TestUseAppContext_GoogleArchitectureOpensource(t *testing.T) {
	appContextPackageName := "google.architecture.opensource.test"
	expected := "google.architecture.opensource.test"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}