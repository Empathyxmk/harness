package public_tests

import (
	"strings"
	"testing"

	"yourmodule/tests/testutil"
)

func TestPublicSimpleArithmeticExpr(t *testing.T) {
	code := "print 20 + 10 + 5;"
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "35") && !strings.Contains(output, "35.0") {
		t.Errorf("Expected output 35 or 35.0, got: %q", output)
	}
}

func TestPublicFloatExprResult(t *testing.T) {
	code := "print 7.5 * 4;"
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "30") && !strings.Contains(output, "30.0") {
		t.Errorf("Expected output 30 or 30.0, got: %q", output)
	}
}