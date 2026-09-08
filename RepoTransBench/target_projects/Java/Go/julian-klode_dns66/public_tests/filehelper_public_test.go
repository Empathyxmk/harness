package public_tests

import (
	"io/ioutil"
	"os"
	"testing"
)

func TestReadFileAndWriteFilePublic(t *testing.T) {
	file, err := ioutil.TempFile("", "dns66test_public_*.txt")
	if err != nil {
		t.Fatalf("cannot create temp file: %v", err)
	}
	defer os.Remove(file.Name())
	defer file.Close()
	data := []byte("public file test data")
	if _, err := file.Write(data); err != nil {
		t.Fatalf("write failed: %v", err)
	}
	file.Sync()
	content, err := ioutil.ReadFile(file.Name())
	if err != nil {
		t.Fatalf("failed to read file: %v", err)
	}
	if string(content) != "public file test data" {
		t.Errorf("expected file content %q, got %q", "public file test data", string(content))
	}

	otherFile, err := ioutil.TempFile("", "dns66test_public_other_*.txt")
	if err != nil {
		t.Fatalf("cannot create temp file: %v", err)
	}
	defer os.Remove(otherFile.Name())
	defer otherFile.Close()

	err = ioutil.WriteFile(otherFile.Name(), []byte("abc_public"), 0644)
	if err != nil {
		t.Fatalf("writeFile failed: %v", err)
	}
	secondRead, err := ioutil.ReadFile(otherFile.Name())
	if err != nil {
		t.Fatalf("failed to read second file: %v", err)
	}
	if string(secondRead) != "abc_public" {
		t.Errorf("expected second file content %q, got %q", "abc_public", string(secondRead))
	}
}

func TestReadFileThrowsPublic(t *testing.T) {
	notAFile := "not_a_real_dns66_filename_public.txt"
	_, err := ioutil.ReadFile(notAFile)
	if err == nil {
		t.Fatalf("expected error reading file that does not exist: %s", notAFile)
	}
}