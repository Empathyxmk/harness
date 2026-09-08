package public_tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Public test: check MANIFEST.in exists and not empty
func TestPublicManifestInExists(t *testing.T) {
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

func TestPublicManifestInHasIncludeOrData(t *testing.T) {
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
	if !strings.Contains(s, "include") &&
		!strings.Contains(s, "data") &&
		!strings.Contains(s, "recursive-include") {
		t.Error("MANIFEST.in does not have include/data/recursive-include statement")
	}
}