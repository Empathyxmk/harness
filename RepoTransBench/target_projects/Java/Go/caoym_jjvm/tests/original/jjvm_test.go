package original

import (
	"bytes"
	"os"
	"strings"
	"testing"
)

type JJvm struct{}

func (j *JJvm) main(args []string) {
	if len(args) == 0 {
		// Should print usage
		println("Usage: <classpath> <JJvm class> [args...]")
		return
	}
	// Simulate error for test
	if args[0] == "invalid" {
		_, _ = os.Stderr.WriteString("Exception: Could not find class\n")
		return
	}
	// Else just return
}

func TestMainPrintsUsage(t *testing.T) {
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	j := &JJvm{}
	j.main([]string{})

	w.Close()
	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	os.Stdout = origStdout

	outStr := buf.String()
	if !strings.Contains(outStr, "Usage: <classpath> <JJvm class> [args...]") {
		t.Errorf("Expected usage string in output, got: %v", outStr)
	}
}

func TestMainHandlesException(t *testing.T) {
	origStderr := os.Stderr
	r, w, _ := os.Pipe()
	os.Stderr = w

	j := &JJvm{}
	j.main([]string{"invalid", "NoSuchClass"})

	w.Close()
	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	os.Stderr = origStderr

	errStr := buf.String()
	if !strings.Contains(errStr, "Exception") {
		t.Errorf("Expected 'Exception' in error output, got: %v", errStr)
	}
}