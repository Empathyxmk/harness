package original

import (
	"strings"
	"testing"

	"yourmodule/tests/testutil"
)

func TestFunction(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("functions_no_args.rpp"))
	if !strings.Contains(output, "Hello from myfunc_one!") {
		t.Errorf("Expected output to contain 'Hello from myfunc_one!', got: %q", output)
	}
}

func TestFunctionReturn(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("function_return.rpp"))
	if !strings.Contains(output, "Value returned from myfunc_one: 100.0") {
		t.Errorf("Expected output to contain 'Value returned from myfunc_one: 100.0', got: %q", output)
	}
}