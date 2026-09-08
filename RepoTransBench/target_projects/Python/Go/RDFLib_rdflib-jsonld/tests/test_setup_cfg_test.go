package tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Test setup.cfg exists and is not empty
func TestSetupCfgExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("could not get CWD: %v", err)
	}
	cfgPath := filepath.Join(cwd, "..", "setup.cfg")
	info, err := os.Stat(cfgPath)
	if err != nil {
		t.Fatalf("setup.cfg missing: %v", err)
	}
	if info.Size() < 10 {
		t.Error("setup.cfg is suspiciously small")
	}
}

// Test setup.cfg mentions metadata or options
func TestSetupCfgMentionsMetadataOrOptions(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	cfgPath := filepath.Join(cwd, "..", "setup.cfg")
	content, err := os.ReadFile(cfgPath)
	if err != nil {
		t.Fatal(err)
	}
	text := string(content)
	if !strings.Contains(text, "[metadata]") && !strings.Contains(text, "[options]") {
		t.Error("setup.cfg does not contain [metadata] or [options] sections")
	}
}