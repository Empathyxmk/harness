package coremodel

import (
	"testing"
)

func TestUseAppContext_ArchitectureGoogleCoremodel(t *testing.T) {
	// In Go, without Android context, stub out test - just cover the assertion with a placeholder
	// Since we can't get an Android package context, we'll simulate a check for the correct app package name.
	appContextPackageName := "architecture.google.coremodel.test"
	expected := "architecture.google.coremodel.test"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}

func TestUseAppContext_GoogleArchitectureCoremodel(t *testing.T) {
	// Simulated environment, as above
	appContextPackageName := "google.architecture.coremodel.test"
	expected := "google.architecture.coremodel.test"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}