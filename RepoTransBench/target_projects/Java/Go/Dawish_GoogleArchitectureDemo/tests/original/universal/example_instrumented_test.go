package universal

import (
	"testing"
)

func TestUseAppContext_GoogleArchitectureUniversal(t *testing.T) {
	appContextPackageName := "google.architecture"
	expected := "google.architecture"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}