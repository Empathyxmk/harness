package original

import (
	"os"
	"strings"
	"testing"
)

// This test simulates "importing" setup.py and ensures metadata fields exist in the file.
func TestSetupPyMetadataFields(t *testing.T) {
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