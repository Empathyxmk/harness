package original

import (
	"os"
	"strings"
	"testing"
)

// This file corresponds to htmlcov/z_a44f0ac069e85531_test_setup_py_py.html

func TestSetupPyExecutionHtmlCov(t *testing.T) {
	contents, err := os.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Could not read setup.py: %v", err)
	}
	if !strings.Contains(string(contents), "setup") {
		t.Error("setup.py does not contain 'setup'")
	}
}

func TestSetupPyMetadataFieldsHtmlCov(t *testing.T) {
	contents, err := os.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Failed to read setup.py: %v", err)
	}
	fields := []string{"author", "name", "url", "version", "packages", "install_requires"}
	for _, key := range fields {
		if !strings.Contains(string(contents), key) {
			t.Errorf("Field %q not found in setup.py", key)
		}
	}
}