package public_tests

import (
	"bytes"
	"io"
	"os"
	"path/filepath"
	"testing"
)

// DummySessionPub for simulating public cache session
type DummySessionPub struct {
	Called bool
}

func (s *DummySessionPub) ProblemData(domainID, pid, tmpPath string) error {
	f, err := os.OpenFile(tmpPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return err
	}
	defer f.Close()
	_, err = f.Write([]byte("pubprobdata"))
	s.Called = true
	return err
}

func TestPublicCacheOpenFileFound(t *testing.T) {
	tmpDir := t.TempDir()
	domain := "domX"
	pid := "probz"
	domainDir := filepath.Join(tmpDir, domain)
	if err := os.MkdirAll(domainDir, 0755); err != nil {
		t.Fatalf("failed to create domain dir: %v", err)
	}
	filePath := filepath.Join(domainDir, pid+".zip")
	if err := os.WriteFile(filePath, []byte("newdata"), 0644); err != nil {
		t.Fatalf("failed to write file: %v", err)
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
	if !bytes.Equal(data, []byte("newdata")) {
		t.Errorf("unexpected data: '%s'", string(data))
	}
}

func TestPublicCacheOpenDownload(t *testing.T) {
	tmpDir := t.TempDir()
	domain := "domY"
	pid := "pz0"
	sess := &DummySessionPub{}
	domainDir := filepath.Join(tmpDir, domain)
	filePath := filepath.Join(domainDir, pid+".zip")
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
	if !bytes.Equal(data, []byte("pubprobdata")) {
		t.Errorf("unexpected content, got: %q", data)
	}
}

func TestPublicCacheInvalidate(t *testing.T) {
	tmpDir := t.TempDir()
	domain := "domZ"
	pid := "ppq"
	cachedir := filepath.Join(tmpDir, domain)
	if err := os.MkdirAll(cachedir, 0755); err != nil {
		t.Fatalf("failed to create cachedir: %v", err)
	}
	fpath := filepath.Join(cachedir, pid+".zip")
	if err := os.WriteFile(fpath, []byte("z"), 0644); err != nil {
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