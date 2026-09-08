package common

import (
	"testing"
)

func TestUseAppContext_GoogleArchitectureCommon(t *testing.T) {
	appContextPackageName := "google.architecture.common.test"
	expected := "google.architecture.common.test"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}