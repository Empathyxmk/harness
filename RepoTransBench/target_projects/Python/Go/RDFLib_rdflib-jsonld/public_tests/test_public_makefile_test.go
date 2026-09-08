package public_tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Public test: docs/Makefile should exist and mention latex or clean
func TestPublicMakefileExistsAndMentionsLatexOrClean(t *testing.T) {
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
		t.Error("docs/Makefile is too small")
	}
	content, err := os.ReadFile(makefilePath)
	if err != nil {
		t.Fatalf("failed to read docs/Makefile: %v", err)
	}
	c := string(content)
	if !strings.Contains(c, "latex") && !strings.Contains(c, "clean") {
		t.Error("docs/Makefile does not mention 'latex' or 'clean'")
	}
}