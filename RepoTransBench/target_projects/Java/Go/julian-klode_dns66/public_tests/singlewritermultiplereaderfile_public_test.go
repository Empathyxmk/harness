package public_tests

import (
	"bytes"
	"io/ioutil"
	"os"
	"testing"
)

func TestStartFinishWritePublic(t *testing.T) {
	file, err := ioutil.TempFile("", "swmr_public_*.txt")
	if err != nil {
		t.Fatalf("cannot create temp file: %v", err)
	}
	defer os.Remove(file.Name())
	defer file.Close()

	data := []byte("abc_public")
	if _, err := file.Write(data); err != nil {
		t.Fatalf("write failed: %v", err)
	}
	file.Sync()
	got, err := ioutil.ReadFile(file.Name())
	if err != nil {
		t.Fatalf("failed to read written file: %v", err)
	}
	if string(got) != "abc_public" {
		t.Errorf("expected %q, got %q", "abc_public", string(got))
	}
}

func TestOpenReadFileNotFoundPublic(t *testing.T) {
	fn := "nonexistent_swmr_public_123.txt"
	_, err := ioutil.ReadFile(fn)
	if err == nil {
		t.Fatalf("expected error reading non-existent file %s", fn)
	}
}