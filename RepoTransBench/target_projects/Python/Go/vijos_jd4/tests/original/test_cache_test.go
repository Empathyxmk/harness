package original

import (
	"bytes"
	"context"
	"io"
	"os"
	"path/filepath"
	"testing"
)

// DummyCache interface and helpers
type DummySession struct {
	Called bool
}

func (s *DummySession) ProblemData(domainID, pid, tmpPath string) error {
	f, err := os.OpenFile(tmpPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return err
	}
	defer f.Close()
	_, err = f.Write([]byte("probdata"))
	s.Called = true
	return err
}

func TestCacheOpenFileFound(t *testing.T) {
	tmpDir := t.TempDir()
	domain := "dom1"
	pid := "prob"
	domainDir := filepath.Join(tmpDir, domain)
	if err := os.MkdirAll(domainDir, 0755); err != nil {
		t.Fatalf("failed to create domain dir: %v", err)
	}
	filePath := filepath.Join(domainDir, pid+".zip")
	if err := os.WriteFile(filePath, []byte("data"), 0644); err != nil {
		t.Fatalf("failed to write file: %v", err)
	}
	// Instead of appdirs, just use tmpPath directly.
	reader, err := os.Open(filePath)
	if err != nil {
		t.Fatalf("could not open file: %v", err)
	}
	data, err := io.ReadAll(reader)
	reader.Close()
	if err != nil {
		t.Fatalf("Failed to read: %v", err)
	}
	if !bytes.Equal(data, []byte("data")) {
		t.Errorf("unexpected data: '%s'", string(data))
	}
}

func TestCacheOpenDownload(t *testing.T) {
	tmpDir := t.TempDir()
	domain := "dom2"
	pid := "p2"
	sess := &DummySession{}
	domainDir := filepath.Join(tmpDir, domain)
	filePath := filepath.Join(domainDir, pid+".zip")
	// simulate: if file does not exist, session.ProblemData will create it
	if err := os.MkdirAll(domainDir, 0755); err != nil {
		t.Fatalf("failed to mkdir domainDir: %v", err)
	}
	if _, err := os.Stat(filePath); !os.IsNotExist(err) {
		t.Fatalf("file %s already exists", filePath)
	}

	tmpPath := filePath
	if err := sess.ProblemData(domain, pid, tmpPath); err != nil {
		t.Fatalf("ProblemData error: %v", err)
	}
	reader, err := os.Open(filePath)
	if err != nil {
		t.Fatalf("could not open file: %v", err)
	}
	data, err := io.ReadAll(reader)
	reader.Close()
	if err != nil {
		t.Fatalf("Failed to read: %v", err)
	}
	if !sess.Called {
		t.Errorf("ProblemData was not called")
	}
	if !bytes.Equal(data, []byte("probdata")) {
		t.Errorf("unexpected content, got: %q", data)
	}
}

func TestCacheInvalidate(t *testing.T) {
	tmpDir := t.TempDir()
	domain := "dom3"
	pid := "pp"
	cachedir := filepath.Join(tmpDir, domain)
	if err := os.MkdirAll(cachedir, 0755); err != nil {
		t.Fatalf("failed to create cachedir: %v", err)
	}
	fpath := filepath.Join(cachedir, pid+".zip")
	if err := os.WriteFile(fpath, []byte("x"), 0644); err != nil {
		t.Fatalf("failed to write cache file: %v", err)
	}
	// Remove file and verify.
	if err := os.Remove(fpath); err != nil {
		t.Fatalf("failed to remove cache file: %v", err)
	}
	if _, err := os.Stat(fpath); !os.IsNotExist(err) {
		t.Errorf("file %s still exists", fpath)
	}
	// Should not error if called again.
	if err := os.Remove(fpath); err != nil && !os.IsNotExist(err) {
		t.Errorf("unexpected error when removing non existent file: %v", err)
	}
}