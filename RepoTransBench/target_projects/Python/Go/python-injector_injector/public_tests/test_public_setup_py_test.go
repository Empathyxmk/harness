package public_tests

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestPublicVersionExists(t *testing.T) {
	versionFile := filepath.Join("setup.py")
	content, err := os.ReadFile(versionFile)
	if err != nil {
		t.Fatalf("failed to read setup.py: %v", err)
	}
	if !strings.Contains(string(content), "version") {
		t.Errorf("expected 'version' to appear in setup.py, but it was not found")
	}
}

func TestPublicDescriptionExists(t *testing.T) {
	setupFile := filepath.Join("setup.py")
	content, err := os.ReadFile(setupFile)
	if err != nil {
		t.Fatalf("failed to read setup.py: %v", err)
	}
	if !strings.Contains(string(content), "description") {
		t.Errorf("expected 'description' to appear in setup.py, but it was not found")
	}
}