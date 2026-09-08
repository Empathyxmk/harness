package original

import (
	"strings"
	"testing"

	"yourmodule/tests/testutil"
)

func TestConditionalExprs(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("if_conditional.rpp"))
	if !strings.Contains(output, "x ( 15.0 ) is equal to 15!") {
		t.Errorf("Expected substring 'x ( 15.0 ) is equal to 15!', got: %q", output)
	}
}

func TestLogicalExprs(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("logical_ops.rpp"))
	if !strings.Contains(output, "x != b:  True") {
		t.Errorf("Expected substring 'x != b:  True', got: %q", output)
	}
}

func TestMathExprs(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("math_ops.rpp"))
	if !strings.Contains(output, "modvar =  1.0") {
		t.Errorf("Expected substring 'modvar =  1.0', got: %q", output)
	}
}