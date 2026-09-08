package public_tests

import (
	"testing"
	"bumpversion"
)

func TestMainModuleImportablePublic(t *testing.T) {
	if !bumpversion.ModuleHasVersion() {
		t.Errorf("Expected bumpversion to have __version__ attribute")
	}
}

func TestVersionPropertyExistencePublic(t *testing.T) {
	s, ok := bumpversion.VersionString()
	if !ok || len(s) == 0 {
		t.Errorf("Expected __version__ to exist and be non-empty string")
	}
}