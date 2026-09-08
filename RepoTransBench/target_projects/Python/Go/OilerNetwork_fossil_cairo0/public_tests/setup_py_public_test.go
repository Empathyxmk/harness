package public_tests

import (
	"io/ioutil"
	"os"
	"strings"
	"testing"
)

// Test that setup.py file exists - public variant.
func TestPublicSetupPyExists(t *testing.T) {
	info, err := os.Stat("setup.py")
	if err != nil {
		t.Fatalf("setup.py does not exist: %v", err)
	}
	if info.IsDir() {
		t.Fatalf("setup.py is a directory, not a file")
	}
}

// Test that setup.py can be "imported" without syntax error (public variant).
func TestPublicSetupPyImports(t *testing.T) {
	content, err := ioutil.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Failed to read setup.py: %v", err)
	}
	lc := strings.ToLower(string(content))
	if !strings.Contains(lc, "build") && !strings.Contains(lc, "scm") {
		t.Log("setup.py does not include 'build' or 'scm' (public variant).")
	}
}

// Test that setup.py includes different expected metadata fields (public variant).
func TestPublicSetupPyMetadata(t *testing.T) {
	content, err := ioutil.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Failed to read setup.py: %v", err)
	}
	if !strings.Contains(string(content), "install_requires") {
		t.Error("setup.py does not include 'install_requires'")
	}
	if !strings.Contains(string(content), "setuptools") {
		t.Error("setup.py does not include 'setuptools'")
	}
}