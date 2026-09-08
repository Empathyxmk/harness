package tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Test that README.md exists and has content
func TestReadmeMdExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("unable to get CWD: %v", err)
	}
	readmePath := filepath.Join(cwd, "..", "README.md")
	fi, err := os.Stat(readmePath)
	if err != nil {
		t.Fatalf("README.md missing: %v", err)
	}
	if fi.Size() < 10 {
		t.Error("README.md has little content")
	}
}

func TestReadmeMdMentionsRDFLib(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	readmePath := filepath.Join(cwd, "..", "README.md")
	content, err := os.ReadFile(readmePath)
	if err != nil {
		t.Fatal(err)
	}
	text := strings.ToLower(string(content))
	if !strings.Contains(text, "rdflib") {
		t.Error("README.md does not mention rdflib")
	}
}