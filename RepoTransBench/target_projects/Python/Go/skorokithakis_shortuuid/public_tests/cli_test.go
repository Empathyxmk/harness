package public

import (
	"bytes"
	"os"
	"os/exec"
	"strings"
	"testing"
)

func runCLI(args ...string) (string, string, error) {
	if len(args) == 0 {
		args = append(args, "generate")
	}
	cmd := exec.Command("shortuuid-cli", args...)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	cmd.Env = append(os.Environ())
	err := cmd.Run()
	return stdout.String(), stderr.String(), err
}

func TestCLIBasicOutput(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found")
	}
	out, errStr, err := runCLI("generate")
	val := strings.TrimSpace(out)
	if val == "" {
		t.Errorf("CLI did not output anything: stdout=%q, stderr=%q, err=%v", out, errStr, err)
	}
}

func TestCLIWithLength(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found")
	}
	out, errStr, err := runCLI("generate", "--length", "19")
	val := strings.TrimSpace(out)
	if len(val) != 19 {
		t.Errorf("Expected length 19, got %d (stderr=%q, err=%v)", len(val), errStr, err)
	}
}

func TestCLIHelp(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found")
	}
	out, errStr, _ := runCLI("--help")
	found := strings.Contains(strings.ToLower(out), "usage:") ||
		strings.Contains(strings.ToLower(errStr), "usage:")
	if !found {
		t.Errorf("No usage message found. Out: %q Err: %q", out, errStr)
	}
}