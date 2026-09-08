package public_tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Public test: check LICENSE.md exists and mentions license
func TestPublicLicenseMdExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("unable to get working dir: %v", err)
	}
	licensePath := filepath.Join(cwd, "..", "LICENSE.md")
	fi, err := os.Stat(licensePath)
	if err != nil {
		t.Fatalf("LICENSE.md missing: %v", err)
	}
	if fi.Size() < 10 {
		t.Error("LICENSE.md is too small")
	}
}

func TestPublicLicenseMdMentionsLicenseWord(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	licensePath := filepath.Join(cwd, "..", "LICENSE.md")
	content, err := os.ReadFile(licensePath)
	if err != nil {
		t.Fatal(err)
	}
	s := strings.ToLower(string(content))
	if !strings.Contains(s, "license") {
		t.Error(`LICENSE.md does not contain the word "license"`)
	}
}