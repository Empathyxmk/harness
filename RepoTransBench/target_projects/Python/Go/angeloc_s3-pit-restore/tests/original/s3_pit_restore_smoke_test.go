package original

import (
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

// TestS3PitRestoreHelp checks s3-pit-restore --help output and exit code.
func TestS3PitRestoreHelp(t *testing.T) {
	exe := getPythonExecutable()
	s3pit := filepath.Join(".", "s3-pit-restore")
	cmd := exec.Command(exe, s3pit, "--help")
	outBytes, err := cmd.CombinedOutput()
	out := string(outBytes)
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			// Even with error, --help should output usage.
		} else {
			t.Fatalf("Failed to execute --help: %v\nOutput:%s", err, out)
		}
	}
	if !strings.Contains(strings.ToLower(out), "usage") {
		t.Errorf("Expected 'usage' in help output, got: %v", out)
	}
	// Ideally: check exit code is 0; Go does not surface exit code on success
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			if ee.ExitCode() != 0 {
				t.Errorf("--help should exit code 0, got: %d", ee.ExitCode())
			}
		}
	}
}

// TestS3PitRestoreMissingBucket tests that running --version (which requires -b option) fails with exit code 2 and appropriate message.
func TestS3PitRestoreMissingBucket(t *testing.T) {
	exe := getPythonExecutable()
	s3pit := filepath.Join(".", "s3-pit-restore")
	cmd := exec.Command(exe, s3pit, "--version")
	cmd.Stderr = nil // let CombinedOutput get both
	outBytes, err := cmd.CombinedOutput()
	out := string(outBytes)
	exitCode := 0
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			exitCode = ee.ExitCode()
		} else {
			t.Fatalf("Error running s3-pit-restore --version: %v", err)
		}
	}
	if exitCode != 2 {
		t.Errorf("Expected exit code 2 for missing bucket, got %d\nOutput: %s", exitCode, out)
	}
	lower := strings.ToLower(out)
	if !(strings.Contains(lower, "required") || strings.Contains(lower, "bucket")) {
		t.Errorf("Expected error message mentioning 'required' or 'bucket', got: %s", out)
	}
}

// getPythonExecutable returns the Python executable to use.
func getPythonExecutable() string {
	python := "python3"
	if runtime.GOOS == "windows" {
		python = "python"
	}
	return python
}