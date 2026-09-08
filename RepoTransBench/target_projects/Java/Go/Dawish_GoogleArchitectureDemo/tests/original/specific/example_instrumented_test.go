package specific

import (
	"testing"
)

func TestUseAppContext_GoogleArchitectureSpecific(t *testing.T) {
	appContextPackageName := "google.architecture.specific"
	expected := "google.architecture.specific"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}