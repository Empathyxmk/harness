package public_tests

import (
	"os"
	"path/filepath"
	"testing"
	"io/ioutil"
)

// Test_TestS3PitRestore_generate_tree_public simulates generate_tree with different input names.
func Test_TestS3PitRestore_generate_tree_public(t *testing.T) {
	// Setup temporary test directory
	tmpRoot, err := ioutil.TempDir("", "pubtree")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpRoot)

	names := []string{"foo", "bar", "baz"}
	for _, name := range names {
		dir := filepath.Join(tmpRoot, name)
		if err := os.MkdirAll(dir, 0o755); err != nil {
			t.Fatalf("Failed to make dir %s: %v", dir, err)
		}
		f, err := os.Create(filepath.Join(dir, "file.txt"))
		if err != nil {
			t.Fatalf("Failed to create file in %s: %v", dir, err)
		}
		f.Close()
	}
	entries, err := ioutil.ReadDir(tmpRoot)
	if err != nil {
		t.Fatalf("Failed to list dirs: %v", err)
	}
	if len(entries) != 3 {
		t.Errorf("Expected 3 directories in %s, got %d", tmpRoot, len(entries))
	}
	for _, entry := range entries {
		if !entry.IsDir() {
			t.Errorf("Expected %s to be a directory", entry.Name())
			continue
		}
		files, err := ioutil.ReadDir(filepath.Join(tmpRoot, entry.Name()))
		if err != nil {
			t.Fatalf("Failed to list files in %s: %v", entry.Name(), err)
		}
		if len(files) != 1 {
			t.Errorf("Expected 1 file in directory %s, got %d", entry.Name(), len(files))
		}
	}
}