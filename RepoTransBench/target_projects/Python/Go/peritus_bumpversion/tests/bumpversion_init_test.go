package tests

import (
	"testing"
	"bumpversion"
)

func TestPublicAPIIncludesDescription(t *testing.T) {
	if !bumpversion.HasDescription() {
		t.Errorf("Expected bumpversion to include DESCRIPTION")
	}
}

func TestMainModuleImportable(t *testing.T) {
	if !bumpversion.MainImportable() {
		t.Errorf("__main__ is not importable")
	}
}