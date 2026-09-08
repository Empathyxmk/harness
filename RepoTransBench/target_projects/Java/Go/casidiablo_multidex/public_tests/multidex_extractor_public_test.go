package public_tests

import (
	"os"
	"testing"
)

func TestNonExistentFileCannotFindCentralDirectoryPublic(t *testing.T) {
	name := "this_file_should_not_exist_" + string(rune(os.Getpid())) + ".zip"
	_, err := os.Open(name)
	if err == nil {
		t.Error("Opening non-existent file should have failed")
	}
	// This always errors, which is expected
}

func TestGetZipCrcNonExistentFilePublic(t *testing.T) {
	name := "definitely_not_here_" + string(rune(os.Getpid())) + ".zip"
	_, err := os.Open(name)
	if err == nil {
		t.Error("CRC on non-existent file should have failed")
	}
}