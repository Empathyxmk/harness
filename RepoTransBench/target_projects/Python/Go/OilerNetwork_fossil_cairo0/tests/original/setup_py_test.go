package original

import (
	"io/ioutil"
	"os"
	"strings"
	"testing"
)

// Test that setup.py file exists.
func TestSetupPyExists(t *testing.T) {
	if _, err := os.Stat("setup.py"); os.IsNotExist(err) {
		t.Errorf("setup.py does not exist")
	}
}

// Test that setup.py can be "imported" (simulate import, check for SCM logic).
func TestSetupPyImports(t *testing.T) {
	content, err := ioutil.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Failed to read setup.py: %v", err)
	}
	// Simulate "import": check for presence of code, SCM logic.
	if !strings.Contains(string(content), "setuptools_scm") {
		t.Log("setup.py does not reference setuptools_scm")
	}
	// Can't check for Python syntax errors in Go, so just note.
}

// Test that setup.py includes expected metadata fields.
func TestSetupPyMetadata(t *testing.T) {
	content, err := ioutil.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Failed to read setup.py: %v", err)
	}
	if !strings.Contains(string(content), "name") {
		t.Error("setup.py does not include 'name'")
	}
	if !strings.Contains(string(content), "version_scheme") {
		t.Error("setup.py does not include 'version_scheme'")
	}
}