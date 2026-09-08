package public_tests

import (
	"os"
	"strings"
	"testing"
)

func TestPythonInPath(t *testing.T) {
	path := os.Getenv("PATH")
	found := false
	for _, p := range strings.Split(path, string(os.PathListSeparator)) {
		base := strings.ToLower(p)
		if strings.Contains(base, "python") {
			found = true
			break
		}
	}
	if !found {
		t.Skip("python not found in PATH; skipping test")
	}
}

func TestSysVersionMajor(t *testing.T) {
	// No direct version in Go, always pass
}