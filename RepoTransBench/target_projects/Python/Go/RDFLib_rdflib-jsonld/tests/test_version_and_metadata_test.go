package tests

import (
	"os"
	"strings"
	"testing"
)

func TestMetadataFields(t *testing.T) {
	f, err := os.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("could not read setup.py: %v", err)
	}
	content := strings.ToLower(string(f))
	if !strings.Contains(content, "version") {
		t.Errorf("setup.py does not contain 'version'")
	}
	if !strings.Contains(content, "author") {
		t.Errorf("setup.py does not contain 'author'")
	}
}