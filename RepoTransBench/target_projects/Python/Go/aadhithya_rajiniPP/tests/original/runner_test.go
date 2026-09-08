package original

import (
	"testing"

	"yourmodule/tests/testutil"
)

func TestExec(t *testing.T) {
	output, _ := testutil.ExecAndCapture(testutil.GetFixturePath("hello_world.rpp"))
	if output != "Hello, World!" {
		t.Fatalf("Expected 'Hello, World!', got: %q", output)
	}
}

func TestEval(t *testing.T) {
	result := testutil.Eval("5+5;")
	if result != 10.0 {
		t.Fatalf("Expected result 10.0, got: %v", result)
	}
}