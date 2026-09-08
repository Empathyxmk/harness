package original

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

func TraceDecorator(fn func(a, b string)) func(a, b string) {
	return func(a, b string) {
		// Simulate printing function call trace
		println("Calling fname with args:", a, b)
		fn(a, b)
	}
}

func TestTraceDecorator(t *testing.T) {
	// Capture stdout
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	fname := TraceDecorator(func(a, b string) {
		// Test function body
	})

	fname("navdeep", "gill")
	w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	io.Copy(&buf, r)

	out := buf.String()
	if !strings.Contains(out, "Calling fname with args:") {
		t.Errorf("Expected trace output, got: %v", out)
	}
	if !strings.Contains(out, "navdeep") || !strings.Contains(out, "gill") {
		t.Errorf("Expected arguments to be in trace, got: %v", out)
	}
}