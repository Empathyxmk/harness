package public_tests

import (
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

// TestS3PitRestoreVersionPublic checks that "-V" acts like "--version" and causes missing bucket error (exit code 2).
func TestS3PitRestoreVersionPublic(t *testing.T) {
	exe := getPythonExecutable()
	s3pit := filepath.Join(".", "s3-pit-restore")
	cmd := exec.Command(exe, s3pit, "-V")
	outBytes, err := cmd.CombinedOutput()
	out := string(outBytes)
	exitCode := 0
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			exitCode = ee.ExitCode()
		} else {
			t.Fatalf("Error running s3-pit-restore -V: %v", err)
		}
	}
	if exitCode != 2 {
		t.Errorf("Expected exit code 2 for missing bucket with -V, got %d\nOutput: %s", exitCode, out)
	}
	lower := strings.ToLower(out)
	if !(strings.Contains(lower, "required") || strings.Contains(lower, "bucket")) {
		t.Errorf("Expected error message mentioning 'required' or 'bucket', got: %s", out)
	}
}

// TestS3PitRestoreInvalidArgPublic checks that invalid arg returns exit code 2 and usage/error.
func TestS3PitRestoreInvalidArgPublic(t *testing.T) {
	exe := getPythonExecutable()
	s3pit := filepath.Join(".", "s3-pit-restore")
	cmd := exec.Command(exe, s3pit, "--notarealarg")
	outBytes, err := cmd.CombinedOutput()
	out := string(outBytes)
	exitCode := 0
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			exitCode = ee.ExitCode()
		} else {
			t.Fatalf("Error running s3-pit-restore --notarealarg: %v", err)
		}
	}
	if exitCode != 2 {
		t.Errorf("Expected exit code 2 for invalid arg, got %d\nOutput: %s", exitCode, out)
	}
	lower := strings.ToLower(out)
	if !(strings.Contains(lower, "usage") || strings.Contains(lower, "error")) {
		t.Errorf("Expected error message about 'usage' or 'error', got: %s", out)
	}
}

func getPythonExecutable() string {
	python := "python3"
	if runtime.GOOS == "windows" {
		python = "python"
	}
	return python
}