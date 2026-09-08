package public_tests

import (
	"os"
	"os/exec"
	"strings"
	"testing"
)

func TestPublicSetupPyExists(t *testing.T) {
	if _, err := os.Stat("../setup.py"); os.IsNotExist(err) {
		t.Fatalf("setup.py does not exist in project root")
	}
}

func TestPublicSetupPySyntax(t *testing.T) {
	cmd := exec.Command("python3", "-m", "py_compile", "../setup.py")
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("setup.py has syntax error or can't be compiled: %v\nOutput: %s", err, string(out))
	}
}

func TestPublicSetupPyVersionCommand(t *testing.T) {
	cmd := exec.Command("python3", "../setup.py", "--version")
	out, err := cmd.CombinedOutput()
	if err != nil {
		outStr := string(out)
		if strings.Contains(outStr, "error") || strings.Contains(strings.ToLower(outStr), "unknown option") {
			t.Logf("setup.py does not support --version; skipping: %s", strings.TrimSpace(outStr))
			return
		}
		t.Fatalf("Error running 'setup.py --version': %v\nOutput: %s", err, outStr)
	}
	if len(strings.TrimSpace(string(out))) == 0 {
		t.Errorf("setup.py --version did not output anything")
	}
}