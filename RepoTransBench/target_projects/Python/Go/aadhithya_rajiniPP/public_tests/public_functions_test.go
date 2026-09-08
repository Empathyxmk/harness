package public_tests

import (
	"strings"
	"testing"

	"yourmodule/tests/testutil"
)

func TestPublicFunctionDifferentContent(t *testing.T) {
	code := `
function greet() {
  print "Public Test Hello!";
}
greet()
`
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "Public Test Hello!") {
		t.Errorf("Expected output to contain 'Public Test Hello!', got: %q", output)
	}
}

func TestPublicFunctionReturnDifferentValue(t *testing.T) {
	code := `
function add(a, b) {
  return a + b;
}
val result = add(75, 125)
print "Public Test - Result: " + result;
`
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "Public Test - Result: 200") && !strings.Contains(output, "Public Test - Result: 200.0") {
		t.Errorf("Expected output with result 200, got: %q", output)
	}
}