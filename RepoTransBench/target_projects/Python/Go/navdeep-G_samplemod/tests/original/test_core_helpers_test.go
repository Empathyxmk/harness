package original

import (
	"bytes"
	"io"
	"os"
	"testing"

	"navdeepG_samplemod/sample"
)

// ---- TestCore ----

func TestGetHmm(t *testing.T) {
	if got := sample.GetHmm(); got != "hmmm..." {
		t.Errorf("GetHmm() = %v, want %v", got, "hmmm...")
	}
}

func TestHmmTrue(t *testing.T) {
	// Capture stdout for check
	r, w, err := os.Pipe()
	if err != nil {
		t.Fatalf("os.Pipe() failed: %v", err)
	}
	stdout := os.Stdout
	defer func() { os.Stdout = stdout }()
	os.Stdout = w

	sample.Hmm()

	w.Close()
	var buf bytes.Buffer
	_, err = io.Copy(&buf, r)
	if err != nil {
		t.Errorf("io.Copy: %v", err)
	}
	output := buf.String()
	output = string(bytes.TrimSpace([]byte(output)))
	expected := "hmmm..."
	if output != expected {
		t.Errorf("Hmm() output = %q, want %q", output, expected)
	}
}

func TestHmmFalse(t *testing.T) {
	// Patch HelpersGetAnswer to false using a closure.
	// Since we can't patch functions in Go easily,
	// we simulate it by temporarily replacing it in sample package.
	// For testing purpose, we expose a testable version here.

	orig := sample.HelpersGetAnswer
	sample.HelpersGetAnswer = func() bool { return false }
	defer func() { sample.HelpersGetAnswer = orig }()

	r, w, err := os.Pipe()
	if err != nil {
		t.Fatalf("os.Pipe() failed: %v", err)
	}
	stdout := os.Stdout
	defer func() { os.Stdout = stdout }()
	os.Stdout = w

	sample.Hmm()
	w.Close()
	var buf bytes.Buffer
	_, err = io.Copy(&buf, r)
	if err != nil {
		t.Errorf("io.Copy: %v", err)
	}
	output := buf.String()
	output = string(bytes.TrimSpace([]byte(output)))
	expected := ""
	if output != expected {
		t.Errorf("Hmm() output with HelpersGetAnswer==false = %q, want %q", output, expected)
	}
}

// ---- TestHelpers ----
func TestGetAnswer(t *testing.T) {
	if !sample.HelpersGetAnswer() {
		t.Error("HelpersGetAnswer() = false, want true")
	}
}