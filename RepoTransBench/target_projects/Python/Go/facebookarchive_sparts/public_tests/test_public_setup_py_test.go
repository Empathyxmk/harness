package public_tests

import (
	"os"
	"testing"
)

func TestPublicReadDummy(t *testing.T) {
	filePath := "defabc.txt"
	data := []byte("sparts test\n")
	if err := os.WriteFile(filePath, data, 0644); err != nil {
		t.Fatalf("failed to write file: %v", err)
	}
	defer os.Remove(filePath)
	content, err := os.ReadFile(filePath)
	if err != nil {
		t.Fatalf("failed to read file: %v", err)
	}
	if string(content) != "sparts test\n" {
		t.Errorf("expected file contents 'sparts test\\n', got '%s'", string(content))
	}
}

func TestPublicExistsDummy(t *testing.T) {
	filePath := "another.txt"
	data := []byte("hello world")
	if err := os.WriteFile(filePath, data, 0644); err != nil {
		t.Fatalf("failed to write file: %v", err)
	}
	defer os.Remove(filePath)
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		t.Errorf("file %s should exist", filePath)
	}
}