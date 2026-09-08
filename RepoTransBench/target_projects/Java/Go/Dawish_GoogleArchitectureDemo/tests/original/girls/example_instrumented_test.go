package girls

import (
	"testing"
)

func TestUseAppContext_GoogleArchitectureGirls(t *testing.T) {
	appContextPackageName := "google.architecture.girls.test"
	expected := "google.architecture.girls.test"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}