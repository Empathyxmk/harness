package public_tests

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// TestSetupPyCanImportAndCallsSetupPublic checks that setup.py exposes author/contact fields.
// Since we can't monkeypatch in Go, we rely on --author flags and output scanning.
func TestSetupPyCanImportAndCallsSetupPublic(t *testing.T) {
	setupPath, err := filepath.Abs("setup.py")
	if err != nil {
		t.Fatalf("Could not determine setup.py path: %v", err)
	}
	if _, err := os.Stat(setupPath); err != nil {
		t.Fatalf("setup.py does not exist at expected path: %v", setupPath)
	}
	// Get author name from setup.py
	cmd := exec.Command("python3", "setup.py", "--author")
	outBytes, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Failed to exec setup.py --author: %v\nOutput: %s", err, outBytes)
	}
	out := string(outBytes)
	if !strings.Contains(out, "Angelo Compagnucci") {
		t.Errorf("Expected 'Angelo Compagnucci' in author output, got: %q", out)
	}

	// Get author email from setup.py
	cmd = exec.Command("python3", "setup.py", "--author-email")
	outBytes, err = cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Failed to exec setup.py --author-email: %v\nOutput: %s", err, outBytes)
	}
	out = string(outBytes)
	if !strings.Contains(out, "angelo.compagnucci@gmail.com") {
		t.Errorf("Expected author email in output, got: %q", out)
	}

	// Keywords flag (usually --keywords but might not be supported, so we parse help)
	cmd = exec.Command("python3", "setup.py", "--help-commands")
	outBytes, err = cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Failed to exec setup.py --help-commands: %v\nOutput: %s", err, outBytes)
	}
	out = string(outBytes)
	if !strings.Contains(out, "keyword") && !strings.Contains(out, "keywords") {
		t.Errorf("Expected 'keywords' or similar field in setup.py help output, got: %q", out)
	}
}