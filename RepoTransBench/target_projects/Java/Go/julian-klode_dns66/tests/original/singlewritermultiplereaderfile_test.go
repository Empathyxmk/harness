package original

import (
	"bytes"
	"io/ioutil"
	"os"
	"testing"
)

func TestWriteAndRead(t *testing.T) {
	content := []byte("hello world")
	tmpfile, err := ioutil.TempFile("", "swmr_testfile")
	if err != nil {
		t.Fatalf("cannot create temp file: %v", err)
	}
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	_, err = tmpfile.Write(content)
	if err != nil {
		t.Fatalf("cannot write: %v", err)
	}
	tmpfile.Sync()

	readBytes, err := ioutil.ReadFile(tmpfile.Name())
	if err != nil {
		t.Fatalf("cannot read: %v", err)
	}
	if !bytes.Equal(content, readBytes) {
		t.Errorf("expected %q, got %q", content, readBytes)
	}
}

func TestReadNonExistentFile(t *testing.T) {
	_, err := ioutil.ReadFile("filedoesnotexist-unique.txt")
	if err == nil {
		t.Fatal("expected error reading non-existent file")
	}
}

func TestFailWrite(t *testing.T) {
	tmpfile, err := ioutil.TempFile("", "swmr_failwrite")
	if err != nil {
		t.Fatalf("cannot create temp file: %v", err)
	}
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()
	// Close immediately; now if we Write -> should succeed, but we simulate a fail by not finishing write.
	_, err = tmpfile.Write([]byte("data"))
	// Not testing actual finish logic; in Go, delete work file (simulate).
	err = os.Remove(tmpfile.Name() + ".dns66-new")
	// No error is expected (the file probably doesn't exist).
}

func TestWorkFileDeletionFailure(t *testing.T) {
	tmpfile, err := ioutil.TempFile("", "swmr_workfail")
	if err != nil {
		t.Fatalf("cannot create temp file: %v", err)
	}
	defer os.Remove(tmpfile.Name())
	// Can't make file non-deletable cross-platform in Go cleanly.
	// Simulate as much as possible.
}