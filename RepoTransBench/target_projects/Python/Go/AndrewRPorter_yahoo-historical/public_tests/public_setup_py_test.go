package public_tests

import (
	"os"
	"strings"
	"testing"
)

func TestSetupPyExecutionPublic(t *testing.T) {
	// Simulate "importing" setup.py.
	contents, err := os.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Could not read setup.py: %v", err)
	}
	if !strings.Contains(string(contents), "setup") {
		t.Error("setup.py does not contain 'setup'")
	}
}

func TestSetupPyMetadataFieldsPublic(t *testing.T) {
	contents, err := os.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("Failed to read setup.py: %v", err)
	}
	fields := []string{"description", "author_email", "download_url"}
	for _, key := range fields {
		if !strings.Contains(string(contents), key) {
			t.Errorf("Field %q not found in setup.py", key)
		}
	}
}