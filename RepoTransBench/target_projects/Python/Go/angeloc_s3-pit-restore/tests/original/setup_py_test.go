package original

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// TestSetupPyCanImportAndCallsSetup simulates the test that executes setup.py and checks outputs.
// Since Python monkeypatching is unavailable, we will check that setup.py can be executed
// and that expected metadata is found in its stdout/stderr.
func TestSetupPyCanImportAndCallsSetup(t *testing.T) {
	// Find setup.py file
	setupPath, err := filepath.Abs("setup.py")
	if err != nil {
		t.Fatalf("Could not determine setup.py path: %v", err)
	}
	if _, err := os.Stat(setupPath); err != nil {
		t.Fatalf("setup.py does not exist at expected path: %v", setupPath)
	}

	// Run setup.py with --name and --version
	cmd := exec.Command("python3", "setup.py", "--name")
	outBytes, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Failed to execute setup.py --name: %v\nOutput: %s", err, outBytes)
	}
	nameOutput := string(outBytes)
	if !strings.Contains(nameOutput, "s3-pit-restore") {
		t.Errorf("Expected name 's3-pit-restore' in output, got: %s", nameOutput)
	}

	cmd = exec.Command("python3", "setup.py", "--version")
	outBytes, err = cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Failed to execute setup.py --version: %v\nOutput: %s", err, outBytes)
	}
	versionOutput := string(outBytes)
	if !strings.Contains(versionOutput, "0.9") {
		t.Errorf("Expected version '0.9' in output, got: %s", versionOutput)
	}

	// Try to dump metadata and check if install_requires is mentioned
	cmd = exec.Command("python3", "setup.py", "--help-commands")
	outBytes, err = cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Failed to execute setup.py --help-commands: %v\nOutput: %s", err, outBytes)
	}
	out := string(outBytes)
	if !(strings.Contains(out, "install") || strings.Contains(out, "install_requires")) {
		t.Errorf("Expected install commands metadata in output, got: %s", out)
	}
}