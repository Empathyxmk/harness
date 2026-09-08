package public

import (
	"strings"
	"testing"
)

func TestPublicCLIInvalidCommand(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found")
	}
	// "notacommand"
	out, errStr, _ := runCLI("notacommand")
	text := (out + errStr)
	text = strings.ToLower(text)
	if !strings.Contains(text, "invalid") && !strings.Contains(text, "unknown") && !strings.Contains(text, "unrecognized") {
		t.Errorf("Expected command error, got: %q", text)
	}
}

func TestPublicCLIDecodeBadString(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found")
	}
	out, errStr, _ := runCLI("decode", "333BADSHORTuuid!")
	text := strings.ToLower(out + errStr)
	if !strings.Contains(text, "error") && !strings.Contains(text, "invalid") && strings.TrimSpace(text) != "" {
		t.Errorf("Expected error or empty output for bad string, got: %q", text)
	}
}

func TestPublicCLIEncodingTooFewArgs(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found")
	}
	out, errStr, _ := runCLI("encode")
	text := strings.ToLower(out + errStr)
	if !(strings.Contains(text, "usage") || strings.Contains(text, "argument") || strings.Contains(text, "error")) {
		t.Errorf("Expected argument/usage error, got: %q", text)
	}
}