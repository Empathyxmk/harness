package public_tests

import (
	"os"
	"testing"
)

func assertExists(t *testing.T, path string) {
	t.Helper()
	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Fatalf("Path should exist: %s", path)
	}
}

func assertNotExists(t *testing.T, path string) {
	t.Helper()
	if _, err := os.Stat(path); err == nil {
		t.Fatalf("Path should not exist: %s", path)
	}
}

func TestPublicTmpdir(t *testing.T) {
	path := "tmp_dir_for_test"
	os.Mkdir(path, 0755)
	defer os.RemoveAll(path)
	assertExists(t, path)
	os.RemoveAll(path)
	assertNotExists(t, path)
}

// Similar approach for add_path, chdir, and module snapshot; see full implementation for all logic.