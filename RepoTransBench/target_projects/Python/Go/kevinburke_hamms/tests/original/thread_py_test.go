package original

import (
	"bytes"
	"os"
	"os/exec"
	"strings"
	"testing"
)

func TestThreadPyImportable(t *testing.T) {
	// In Go, importability is handled by compiler; simulate with a dummy operation.
	// If this test runs, the file is importable.
}

func TestThreadPyMain(t *testing.T) {
	// We'll run the program (`go run thread.go`) and check output
	cmd := exec.Command("go", "run", "thread.go")
	var stdout bytes.Buffer
	cmd.Stdout = &stdout
	err := cmd.Run()
	if err != nil {
		t.Fatalf("Error running thread.go: %v", err)
	}
	out := stdout.String()
	if !strings.Contains(out, "HammsServer started") {
		t.Errorf("Expected output to contain 'HammsServer started', got: %v", out)
	}
	if !strings.Contains(out, "stopping") {
		t.Errorf("Expected output to contain 'stopping', got: %v", out)
	}
	if !strings.Contains(out, "HammsServer stopped") {
		t.Errorf("Expected output to contain 'HammsServer stopped', got: %v", out)
	}
}