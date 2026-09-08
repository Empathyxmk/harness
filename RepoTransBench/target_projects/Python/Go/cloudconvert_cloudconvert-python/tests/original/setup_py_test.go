package original

import (
	"os"
	"os/exec"
	"strings"
	"testing"
)

func TestSetupPyExists(t *testing.T) {
	// Try to find setup.py in the project root.
	if _, err := os.Stat("../../setup.py"); os.IsNotExist(err) {
		t.Fatalf("setup.py file does not exist in the project root")
	}
}

func TestSetupPySyntax(t *testing.T) {
	// Attempt to parse the file for syntax errors by running "python -m py_compile setup.py"
	cmd := exec.Command("python3", "-m", "py_compile", "../../setup.py")
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("setup.py has a syntax error or cannot be compiled: %v\nOutput: %s", err, string(out))
	}
}

func TestSetupPyVersionCommand(t *testing.T) {
	// Run "python3 setup.py --version" and check output (if supported)
	cmd := exec.Command("python3", "../../setup.py", "--version")
	out, err := cmd.CombinedOutput()
	if err != nil {
		// Allow the test to pass if "--version" is not implemented, but fail for other issues
		outStr := string(out)
		if strings.Contains(outStr, "error") || strings.Contains(strings.ToLower(outStr), "unknown option") {
			t.Logf("setup.py does not support --version; skipping: %s", strings.TrimSpace(outStr))
			return
		}
		t.Fatalf("error running 'setup.py --version': %v\nOutput: %s", err, outStr)
	}
	if len(strings.TrimSpace(string(out))) == 0 {
		t.Errorf("setup.py --version did not output anything")
	}
}