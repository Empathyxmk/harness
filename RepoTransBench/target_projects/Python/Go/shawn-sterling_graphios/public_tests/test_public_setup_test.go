package public_tests

import (
	"os"
	"path/filepath"
	"testing"
)

func TestPublicSetupPyRuns(t *testing.T) {
	dir, _ := os.Getwd()
	setupPath := filepath.Join(dir, "../setup.py")
	if _, err := os.Stat(setupPath); err != nil {
		t.Fatalf("setup.py file does not exist at %s", setupPath)
	}
}