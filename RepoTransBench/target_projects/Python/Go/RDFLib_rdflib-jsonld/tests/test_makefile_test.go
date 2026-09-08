package tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Test docs/Makefile exists and is not empty
func TestMakefileExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("could not get CWD: %v", err)
	}
	makefilePath := filepath.Join(cwd, "..", "docs", "Makefile")
	info, err := os.Stat(makefilePath)
	if err != nil {
		t.Fatalf("docs/Makefile missing: %v", err)
	}
	if info.Size() < 10 {
		t.Error("docs/Makefile is suspiciously small")
	}
}

// Test Makefile mentions sphinx or html
func TestMakefileMentionsSphinxOrHtml(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	makefilePath := filepath.Join(cwd, "..", "docs", "Makefile")
	content, err := os.ReadFile(makefilePath)
	if err != nil {
		t.Fatal(err)
	}
	text := string(content)
	if !strings.Contains(text, "sphinx") && !strings.Contains(text, "html") {
		t.Error("docs/Makefile does not mention 'sphinx' or 'html'")
	}
}