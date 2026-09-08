package coremodel

import (
	"testing"
)

func TestAdditionIsCorrect_ArchitectureGoogleCoremodel(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("2 + 2 should equal 4")
	}
}

func TestAdditionIsCorrect_GoogleArchitectureCoremodel(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("2 + 2 should equal 4")
	}
}