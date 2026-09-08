package original

import (
	"os"
	"path/filepath"
	"testing"
)

// Dummy ObfDex "obf" function
func ObfDexObf(path string, n int, a []string, b []string, c interface{}) {
	// In original code: simulate directory/file handling without errors.

	info, err := os.Stat(path)
	if err != nil {
		// Path does not exist, do nothing
		return
	}
	if info.IsDir() {
		f, _ := os.Open(path)
		files, _ := f.Readdirnames(-1)
		_ = files
		// Simulate operation on empty/non-empty directories
	} else if filepath.Ext(path) != ".dex" {
		// Should do nothing (not a dex file)
	}
	// Does not throw/panic in any case
}

func TestObfNonExistentDir(t *testing.T) {
	ObfDexObf("not/a/real/directory", 1, []string{}, []string{}, nil)
}

func TestObfSingleFileThatIsNotDex(t *testing.T) {
	tmp, err := os.CreateTemp("", "notadex*.txt")
	if err != nil {
		t.Fatalf("failed to create temp file: %v", err)
	}
	tmpPath := tmp.Name()
	tmp.Close()

	defer os.Remove(tmpPath)
	ObfDexObf(tmpPath, 1, []string{}, []string{}, nil)
}

func TestObfEmptyDirectory(t *testing.T) {
	dir := filepath.Join(os.TempDir(), "empty_dir_for_obf_test")
	_ = os.RemoveAll(dir) // always fresh
	err := os.Mkdir(dir, 0o755)
	if err != nil && !os.IsExist(err) {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(dir)
	ObfDexObf(dir, 1, []string{}, []string{}, nil)
}