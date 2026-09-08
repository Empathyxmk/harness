package public_tests

import (
	"strings"
	"testing"
)

func getFileNameFromPath(path string) string {
	slash := strings.LastIndex(path, "/")
	if slash == -1 {
		return path
	}
	return path[slash+1:]
}

func getFileExtension(filename string) string {
	pos := strings.LastIndex(filename, ".")
	if pos == -1 {
		return ""
	}
	return filename[pos+1:]
}

func isAbsolutePath(path string) bool {
	return strings.HasPrefix(path, "/")
}

func TestFilePathExtractionPublic(t *testing.T) {
	filePath := "/storage/emulated/0/Download/public_test_file2.txt"
	fileName := getFileNameFromPath(filePath)
	if fileName != "public_test_file2.txt" {
		t.Errorf("FileName extraction error: %q", fileName)
	}
}

func TestGetFileExtensionPublic(t *testing.T) {
	fileName := "sample_document.data"
	ext := getFileExtension(fileName)
	if ext != "data" {
		t.Errorf("File extension error: got %q", ext)
	}
}

func TestIsPathAbsolutePublic(t *testing.T) {
	path := "/home/user/example"
	if !isAbsolutePath(path) {
		t.Error("Should be absolute")
	}
	relPath := "docs/readme.txt"
	if isAbsolutePath(relPath) {
		t.Error("Should not be absolute")
	}
}