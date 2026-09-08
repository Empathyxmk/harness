package public_tests

import (
	"testing"

	"yourmodule/rajinipp/runner"
)

func TestPublicRunnerTokenizeAndExec(t *testing.T) {
	rppRunner := runner.NewRppRunner()
	code := "print 1234;"
	output, _ := rppRunner.ExecAndCapture(code)
	if !contains(output, "1234") {
		t.Errorf("Expected output to contain 1234, got: %q", output)
	}
}

func TestPublicRunnerEvalSimpleLine(t *testing.T) {
	rppRunner := runner.NewRppRunner()
	result := rppRunner.Eval("10 + 50")
	if result != 60.0 && result != 60 {
		t.Errorf("Expected 60 or 60.0, got: %v", result)
	}
}

// Helper
func contains(s, substr string) bool {
	return len(substr) == 0 || (len(s) >= len(substr) && (strings.Index(s, substr) != -1))
}