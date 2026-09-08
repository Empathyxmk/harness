package public_tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Public test: setup.cfg should exist and contain at least one section header
func TestPublicSetupCfgExistsAndContainsSection(t *testing.T) {
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
		t.Error("setup.cfg is too small")
	}
	content, err := os.ReadFile(cfgPath)
	if err != nil {
		t.Fatalf("failed to read setup.cfg: %v", err)
	}
	c := string(content)
	if !strings.Contains(c, "[") || !strings.Contains(c, "]") {
		t.Error("setup.cfg does not contain any [section]")
	}
}