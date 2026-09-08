package public_tests

import (
	"os"
	"strings"
	"testing"
	"path/filepath"
)

// Public test: check README.md exists and has content
func TestPublicReadmeMdExists(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("unable to get working dir: %v", err)
	}
	readmePath := filepath.Join(cwd, "..", "README.md")
	fi, err := os.Stat(readmePath)
	if err != nil {
		t.Fatalf("README.md missing: %v", err)
	}
	if fi.Size() < 10 {
		t.Error("README.md is too small")
	}
}

func TestPublicReadmeMdMentionsJSONLD(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	readmePath := filepath.Join(cwd, "..", "README.md")
	content, err := os.ReadFile(readmePath)
	if err != nil {
		t.Fatal(err)
	}
	s := strings.ToLower(string(content))
	if !strings.Contains(s, "jsonld") && !strings.Contains(s, "json-ld") {
		t.Error("README.md does not mention jsonld or json-ld")
	}
}