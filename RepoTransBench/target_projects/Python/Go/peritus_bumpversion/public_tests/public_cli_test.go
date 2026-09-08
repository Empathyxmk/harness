package public_tests

import (
	"os/exec"
	"strings"
	"testing"
)

func TestHelpInvocationCLIPublic(t *testing.T) {
	cmd := exec.Command("go", "run", "../bumpversion/main.go", "--help")
	out, err := cmd.CombinedOutput()
	output := strings.ToLower(string(out))
	if !(strings.Contains(output, "usage") || strings.Contains(output, "help")) {
		t.Errorf("Expected usage/help in output, got: %v", output)
	}
	if err != nil && !strings.Contains(output, "--help") {
		t.Errorf("unexpected error %v: %v", err, output)
	}
}