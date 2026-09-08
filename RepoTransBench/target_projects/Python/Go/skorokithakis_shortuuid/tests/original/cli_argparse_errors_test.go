package original

import (
	"bytes"
	"os"
	"os/exec"
	"strings"
	"testing"
)

func TestCLIInvalidArguments(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found in PATH")
	}
	{
		// (1) Unknown subcommand
		out, err := runShortUUIDCLI("bogus")
		if err == nil {
			t.Errorf("CLI should fail with invalid subcommand, got output: %q", out)
		}
		found := strings.Contains(strings.ToLower(out), "invalid") ||
			strings.Contains(strings.ToLower(out), "unknown") ||
			strings.Contains(strings.ToLower(out), "unrecognized")
		if !found {
			t.Errorf("CLI error string for invalid subcommand missing, output: %q", out)
		}
	}
	{
		// (2) 'encode' with no UUID
		out, err := runShortUUIDCLI("encode")
		if err == nil {
			t.Errorf("CLI should fail with encode missing argument, got output: %q", out)
		}
		low := strings.ToLower(out)
		if !strings.Contains(low, "usage") && !strings.Contains(low, "argument") && !strings.Contains(low, "error") {
			t.Errorf("CLI error expected for missing encode arg, got: %q", out)
		}
	}
	{
		// (3) 'decode' with no shortuuid arg
		out, err := runShortUUIDCLI("decode")
		if err == nil {
			t.Errorf("CLI should fail with decode missing argument, got output: %q", out)
		}
		low := strings.ToLower(out)
		if !strings.Contains(low, "usage") && !strings.Contains(low, "argument") && !strings.Contains(low, "error") {
			t.Errorf("CLI error expected for missing decode arg, got: %q", out)
		}
	}
}