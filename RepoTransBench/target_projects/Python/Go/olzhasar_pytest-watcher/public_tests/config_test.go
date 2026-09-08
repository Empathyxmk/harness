package public_tests

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
)

type Config struct {
	Path string
}

func TestConfigCustomPath(t *testing.T) {
	tmpdir := os.TempDir()
	tmpfile := filepath.Join(tmpdir, "different_test_pyproject.toml")
	content := []byte("[tool.pytest-watcher]\n")
	err := ioutil.WriteFile(tmpfile, content, 0644)
	if err != nil {
		t.Fatalf("Could not create tmp file: %v", err)
	}
	conf := &Config{Path: tmpfile}
	if conf.Path != tmpfile {
		t.Errorf("Config.Path = %v, want %v", conf.Path, tmpfile)
	}
	_ = os.Remove(tmpfile)
}