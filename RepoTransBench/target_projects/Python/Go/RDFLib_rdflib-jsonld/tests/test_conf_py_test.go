package tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Test that docs/conf.py exists and is not empty
func TestConfPyExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("could not get CWD: %v", err)
	}
	confPath := filepath.Join(cwd, "..", "docs", "conf.py")
	info, err := os.Stat(confPath)
	if err != nil {
		t.Fatalf("docs/conf.py missing: %v", err)
	}
	if info.Size() < 10 {
		t.Error("docs/conf.py is suspiciously small")
	}
}

// Test that conf.py mentions project or version
func TestConfPyMentionsProjectOrVersion(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	confPath := filepath.Join(cwd, "..", "docs", "conf.py")
	content, err := os.ReadFile(confPath)
	if err != nil {
		t.Fatal(err)
	}
	text := string(content)
	if !strings.Contains(text, "project") && !strings.Contains(text, "version") {
		t.Error("docs/conf.py does not mention 'project' or 'version'")
	}
}