package tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Test that MANIFEST.in exists and is not empty
func TestManifestInExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("unable to get working dir: %v", err)
	}
	manifestPath := filepath.Join(cwd, "..", "MANIFEST.in")
	fi, err := os.Stat(manifestPath)
	if err != nil {
		t.Fatalf("MANIFEST.in missing: %v", err)
	}
	if fi.Size() == 0 {
		t.Error("MANIFEST.in is empty")
	}
}

// Test MANIFEST.in contains an include or recursive-include statement
func TestManifestInHasInclude(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	manifestPath := filepath.Join(cwd, "..", "MANIFEST.in")
	content, err := os.ReadFile(manifestPath)
	if err != nil {
		t.Fatal(err)
	}
	s := string(content)
	if !strings.Contains(s, "include") && !strings.Contains(s, "recursive-include") {
		t.Error("MANIFEST.in does not have include/recursive-include statement")
	}
}