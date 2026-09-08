package public_tests

import (
	"bytes"
	"os/exec"
	"strings"
	"testing"
)

func TestThreadPyImportableCustom(t *testing.T) {
	// In Go, importability is handled by compiler; simulate with a dummy operation.
	// If code compiles and test runs, importable.
}

func TestThreadPyMainCustom(t *testing.T) {
	// Run the thread.go example and check output for "started" and "stop"
	cmd := exec.Command("go", "run", "thread.go")
	var stdout bytes.Buffer
	cmd.Stdout = &stdout
	err := cmd.Run()
	if err != nil {
		t.Fatalf("Error running thread.go: %v", err)
	}
	lines := strings.Split(strings.TrimSpace(stdout.String()), "\n")
	foundStart := false
	for _, l := range lines {
		if strings.Contains(l, "HammsServer started") {
			foundStart = true
			break
		}
	}
	if !foundStart {
		t.Errorf("Expected some line to contain 'HammsServer started'")
	}
	if len(lines) < 2 {
		t.Fatalf("Expected at least 2 lines for stopping/stop, got %v", lines)
	}
	if strings.TrimSpace(strings.ToLower(lines[len(lines)-2])) != "stopping" {
		t.Errorf("Expected 'stopping' as second-to-last line, got %v", lines[len(lines)-2])
	}
	if !strings.Contains(lines[len(lines)-1], "HammsServer stopped") {
		t.Errorf("Expected last line to be 'HammsServer stopped'")
	}
}