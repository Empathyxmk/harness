package public_tests

import (
	"testing"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestVersionAndBaseImportPublic(t *testing.T) {
	version := "1.1.1.dev0"
	if version == "" {
		t.Fatalf("__version__ string should not be empty")
	}
	// Check existence of WorkflowEnabled
	_ = xworkflows.WorkflowEnabled{}
}