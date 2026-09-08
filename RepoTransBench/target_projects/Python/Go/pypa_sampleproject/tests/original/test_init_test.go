package original

import (
	"bytes"
	"os"
	"testing"
	"pypa_sampleproject/src/sample"
)

func TestMainPrintsMessage(t *testing.T) {
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
	if out == "" || !contains(out, "Call your main application code here") {
		t.Fatalf("Output missing expected message. Got: %q", out)
	}
}

// Contains helper for string in string (case sensitive)
func contains(s, substr string) bool {
	return len(substr) == 0 || (len(s) >= len(substr) && (s == substr || len(s) > len(substr) && (s[:len(substr)] == substr || contains(s[1:], substr))))
}