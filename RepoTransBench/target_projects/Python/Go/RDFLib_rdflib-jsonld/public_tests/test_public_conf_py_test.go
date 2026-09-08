package public_tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Public test: docs/conf.py should exist and mention copyright
func TestPublicConfPyExistsAndMentionsCopyright(t *testing.T) {
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
		t.Error("docs/conf.py is very small")
	}
	content, err := os.ReadFile(confPath)
	if err != nil {
		t.Fatalf("failed to read docs/conf.py: %v", err)
	}
	if !strings.Contains(string(content), "copyright") {
		t.Error("docs/conf.py does not mention 'copyright'")
	}
}