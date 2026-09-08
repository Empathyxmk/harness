package original

import (
	"bytes"
	"os/exec"
	"strings"
	"testing"
)

func TestImportHammsMain(t *testing.T) {
	// In Go, can import the module directly (already done by build).
	// This test just checks import does not panic.
}

func TestMainFunction(t *testing.T) {
	// Run go code that prints "hamms main executed" and capture its output.
	cmd := exec.Command("go", "run", "./hamms/main_stub.go")
	var stdout bytes.Buffer
	cmd.Stdout = &stdout
	err := cmd.Run()
	if err != nil {
		t.Fatalf("Error running hamms main: %v", err)
	}
	out := stdout.String()
	if !strings.Contains(out, "hamms main executed") {
		t.Errorf("Expected output to contain 'hamms main executed', got: %v", out)
	}
}