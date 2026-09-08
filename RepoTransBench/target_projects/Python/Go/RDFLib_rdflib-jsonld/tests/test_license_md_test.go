package tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Test that LICENSE.md exists and contains a license-like string
func TestLicenseMdExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("unable to get CWD: %v", err)
	}
	licensePath := filepath.Join(cwd, "..", "LICENSE.md")
	fi, err := os.Stat(licensePath)
	if err != nil {
		t.Fatalf("LICENSE.md missing: %v", err)
	}
	if fi.Size() < 10 {
		t.Error("LICENSE.md is too small, likely invalid")
	}
}

func TestLicenseMdContainsLicense(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	licensePath := filepath.Join(cwd, "..", "LICENSE.md")
	content, err := os.ReadFile(licensePath)
	if err != nil {
		t.Fatal(err)
	}
	text := strings.ToLower(string(content))
	if !(strings.Contains(text, "license") || strings.Contains(text, "copyright")) {
		t.Error(`LICENSE.md does not contain "license" nor "copyright"`)
	}
}