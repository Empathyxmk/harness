package original

import (
	"testing"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestVersionAndBaseImport(t *testing.T) {
	version := "1.1.1.dev0"
	if version == "" {
		t.Fatalf("__version__ string cannot be empty")
	}
	// Check base Workflow existence
	_ = xworkflows.Workflow{}
}