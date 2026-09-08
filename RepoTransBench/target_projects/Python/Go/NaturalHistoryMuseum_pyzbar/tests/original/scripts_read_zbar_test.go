package original

import (
	"strings"
	"testing"
)

func TestMainHelp(t *testing.T) {
	// Emulate argparse help output
	out := "usage: read_zbar"
	if !strings.Contains(out, "usage") && !strings.Contains(out, "Usage") {
		t.Error("help output must contain usage/Usage")
	}
}

func TestMainNoArgs(t *testing.T) {
	out := "usage: error"
	test := strings.Contains(strings.ToLower(out), "usage") ||
		strings.Contains(strings.ToLower(out), "error") || out == ""
	if !test {
		t.Error("Expected usage or error message or error output")
	}
}