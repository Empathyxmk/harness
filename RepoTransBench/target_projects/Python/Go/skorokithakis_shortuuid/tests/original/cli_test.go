package original

import (
	"bytes"
	"os"
	"os/exec"
	"strings"
	"testing"

	"github.com/google/uuid"
)

// Assumes a CLI called "shortuuid-cli" is implemented in Go that accepts similar commands
func runShortUUIDCLI(args ...string) (string, error) {
	var stdout, stderr bytes.Buffer
	cmd := exec.Command("shortuuid-cli", args...)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	cmd.Env = append(os.Environ())
	err := cmd.Run()
	if err != nil {
		return stdout.String() + stderr.String(), err
	}
	return stdout.String(), nil
}

func TestCLIEncodeAndDecode(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found in PATH; skipping CLI integration test.")
	}
	// 1. Encode a UUID
	u := uuid.New()
	outEncode, err := runShortUUIDCLI("encode", u.String())
	if err != nil {
		t.Fatalf("CLI encode failed: %v\nOutput: %s", err, outEncode)
	}
	code := strings.TrimSpace(outEncode)
	if code == "" {
		t.Fatal("No output from CLI encode")
	}

	// Output should be valid shortuuid string (validate is string and not empty)
	if len(code) == 0 {
		t.Error("ShortUUID code is empty")
	}

	// 2. Decode the code to get the original UUID
	outDecode, err := runShortUUIDCLI("decode", code)
	if err != nil {
		t.Fatalf("CLI decode failed: %v\nOutput: %s", err, outDecode)
	}
	decoded := strings.TrimSpace(outDecode)
	if _, err := uuid.Parse(decoded); err != nil {
		t.Errorf("Failed to parse decoded value as UUID: got '%s', err: %v", decoded, err)
	}
}

// Assumes the CLI accepts a --legacy flag for decode
func TestCLIDecodeLegacy(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found; skipping CLI integration test.")
	}
	u := uuid.New()
	code := encodeUUIDForTest(u)
	rev := reverseString(code)
	out, err := runShortUUIDCLI("decode", rev, "--legacy")
	if err != nil {
		t.Fatalf("CLI decode legacy failed: %v, output: %s", err, out)
	}
	out = strings.TrimSpace(out)
	if _, err := uuid.Parse(out); err != nil {
		t.Errorf("Failed to decode legacy reversed string: %v", err)
	}
}

// Helper for encoding (needs real shortuuid implementation)
func encodeUUIDForTest(u uuid.UUID) string {
	// TODO: Replace this implementation with your actual encode logic
	return u.String() // Placeholder
}

func reverseString(s string) string {
	// Helper: reverse a string
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func TestCLINoFn(t *testing.T) {
	if _, err := exec.LookPath("shortuuid-cli"); err != nil {
		t.Skip("shortuuid-cli binary not found in PATH; skipping CLI integration test.")
	}
	outstr, err := runShortUUIDCLI()
	if err != nil {
		t.Fatalf("CLI no-arg call failed: %v, output: %s", err, outstr)
	}
	outstr = strings.TrimSpace(outstr)
	if outstr == "" {
		t.Error("CLI should output a non-empty string")
	}
}