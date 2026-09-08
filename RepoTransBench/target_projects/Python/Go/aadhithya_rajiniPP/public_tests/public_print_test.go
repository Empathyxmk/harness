package public_tests

import (
	"strings"
	"testing"

	"yourmodule/tests/testutil"
)

func TestPublicPrintSimpleMessage(t *testing.T) {
	code := `print "Public output!";`
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "Public output!") {
		t.Errorf("Expected output 'Public output!', got: %q", output)
	}
}

func TestPublicPrintNumberAndStringConcat(t *testing.T) {
	code := `val score = 99
print "Score: " + score;`
	output, _ := testutil.ExecCodeString(code)
	if !strings.Contains(output, "Score: 99") {
		t.Errorf("Output should contain 'Score: 99', got: %q", output)
	}
}