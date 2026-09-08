package public_tests

import (
	"os"
	"path/filepath"
	"testing"

	"antiboredom_audiogrep/audiogrep"
)

func TestGetFilesPublic(t *testing.T) {
	tmpdir := t.TempDir()
	a := filepath.Join(tmpdir, "file1.aac")
	b := filepath.Join(tmpdir, "file2.m4a")
	c := filepath.Join(tmpdir, "file3.txt")
	files := []string{a, b, c}
	for _, f := range files {
		err := os.WriteFile(f, []byte("test abc"), 0644)
		if err != nil {
			t.Fatal(err)
		}
	}
	fs := map[string]bool{}
	for _, f := range audiogrep.GetFiles(tmpdir, []string{".aac", ".m4a"}) {
		fs[f] = true
	}
	expected := map[string]bool{a: true, b: true}
	if len(fs) != 2 || !fs[a] || !fs[b] {
		t.Errorf("Expected: %+v, got %+v", expected, fs)
	}
}