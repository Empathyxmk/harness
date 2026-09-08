package public_tests

import (
	"strings"
	"testing"

	"yourmodule/tests/testutil"
)

func TestPublicIfStatementTrueBranch(t *testing.T) {
	code := `
val x = 6
if (x % 2 == 0) {
    print "even-case!";
}
`
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "even-case!") {
		t.Errorf("Output should contain 'even-case!', got: %q", output)
	}
}

func TestPublicWhileLoopPrint(t *testing.T) {
	code := `
val count = 0
while (count < 2) {
    print "loop: " + count;
    count = count + 1;
}
`
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "loop: 0") {
		t.Error("Output should contain 'loop: 0'")
	}
	if !strings.Contains(output, "loop: 1") {
		t.Error("Output should contain 'loop: 1'")
	}
}