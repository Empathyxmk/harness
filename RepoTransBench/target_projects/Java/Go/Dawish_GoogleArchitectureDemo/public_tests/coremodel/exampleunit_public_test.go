package coremodel

import "testing"

func TestAdditionIsCorrectWithDifferentData_ArchitectureGoogleCoremodel(t *testing.T) {
	if 3+3 != 6 {
		t.Errorf("expected 3 + 3 == 6")
	}
}

func TestAdditionIsCorrectWithDifferentData_GoogleArchitectureCoremodel(t *testing.T) {
	if 20+5 != 25 {
		t.Errorf("expected 20 + 5 == 25")
	}
}