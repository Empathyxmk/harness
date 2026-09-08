package public_tests

import (
	"bytes"
	"os"
	"testing"
	"pypa_sampleproject/src/sample"
	"strings"
)

func TestMainPrintsCustomMessage(t *testing.T) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	sample.Main()

	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	_, err := buf.ReadFrom(r)
	if err != nil {
		t.Fatalf("Error reading from pipe: %v", err)
	}
	out := buf.String()
	if !strings.Contains(out, "main application code") {
		t.Fatalf("Output missing expected message substring. Got: %q", out)
	}
}