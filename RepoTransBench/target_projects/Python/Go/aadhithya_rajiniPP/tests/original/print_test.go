package original

import (
	"testing"

	"yourmodule/tests/testutil"
)

func TestPrint(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("hello_world.rpp"))
	if output != "Hello, World!" {
		t.Fatalf("Expected output 'Hello, World!', got: %q", output)
	}
}

func TestMultiPrint(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("multi_print.rpp"))
	if output != "5 + 5 = 10.0" {
		t.Errorf("Expected output '5 + 5 = 10.0', got: %q", output)
	}
}