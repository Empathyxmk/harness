package coremodel

import (
	"testing"
)

func TestUseAppContextWithDifferentData_ArchitectureGoogleCoremodel(t *testing.T) {
	appContextPackageName := "architecture.google.coremodel.test"
	badExpected := "architecture.google.coremodel"
	if appContextPackageName == badExpected {
		t.Errorf("expected package name NOT to be %s", badExpected)
	}
}

func TestUseAppContextWithDifferentData_GoogleArchitectureCoremodel(t *testing.T) {
	appContextPackageName := "google.architecture.coremodel.test"
	badExpected := "google.architecture.coremodel"
	if appContextPackageName == badExpected {
		t.Errorf("expected package name NOT to be %s", badExpected)
	}
}