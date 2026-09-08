package original

import (
	"strings"
	"testing"

	"yourmodule/tests/testutil"
)

func TestIf(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("if_conditional.rpp"))
	if !strings.Contains(output, "x ( 15.0 ) is equal to 15!") {
		t.Errorf("Expected substring 'x ( 15.0 ) is equal to 15!', got: %q", output)
	}
}

func TestIfElse(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("if_else_conditional.rpp"))
	if !strings.Contains(output, "x ( 5.0 ) is less than 10!") {
		t.Errorf("Expected substring 'x ( 5.0 ) is less than 10!', got: %q", output)
	}
}

func TestForLoop(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("for_loop.rpp"))
	if !strings.Contains(output, "After loop: X = 14.0") {
		t.Errorf("Expected substring 'After loop: X = 14.0', got: %q", output)
	}
}

func TestWhileLoop(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("while_loop.rpp"))
	if !strings.Contains(output, "breaking out of loop...") {
		t.Errorf("Expected substring 'breaking out of loop...', got: %q", output)
	}
}