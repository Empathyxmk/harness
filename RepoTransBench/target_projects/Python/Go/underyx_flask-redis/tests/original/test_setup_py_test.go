package original

import (
	"errors"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
	"regexp"
)

// Helper function for the Python 'read'
func readFile(paths ...string) (string, error) {
	if len(paths) == 0 {
		return "", errors.New("no path provided")
	}
	fullPath := filepath.Join(paths...)
	data, err := ioutil.ReadFile(fullPath)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func TestReadReadsFile(t *testing.T) {
	dir := t.TempDir()
	pkgDir := filepath.Join(dir, "flask_redis")
	err := os.Mkdir(pkgDir, 0o755)
	if err != nil && !os.IsExist(err) {
		t.Fatalf("Failed to create directory: %v", err)
	}
	filePath := filepath.Join(pkgDir, "dummy.py")
	testText := "abc"
	if err := ioutil.WriteFile(filePath, []byte(testText), 0644); err != nil {
		t.Fatalf("Failed to write file: %v", err)
	}
	result, err := readFile(filePath)
	if err != nil {
		t.Fatalf("Failed to read via readFile: %v", err)
	}
	if result != testText {
		t.Errorf("Expected '%s', got '%s'", testText, result)
	}
}

// Simulate 'find_meta' with success
func TestFindMetaSuccess(t *testing.T) {
	content := "__title__ = 'foo'\n__description__ = 'bar'"
	findMeta := func(meta, content string) (string, error) {
		re := regexp.MustCompile(`__` + regexp.QuoteMeta(meta) + `__\s*=\s*['"]([^'"]*)['"]`)
		match := re.FindStringSubmatch(content)
		if len(match) > 1 {
			return match[1], nil
		}
		return "", errors.New("Unable to find __" + meta + "__ string.")
	}
	result1, err1 := findMeta("title", content)
	if err1 != nil {
		t.Fatalf("Expected to find 'title': %v", err1)
	}
	result2, err2 := findMeta("description", content)
	if err2 != nil {
		t.Fatalf("Expected to find 'description': %v", err2)
	}
	if result1 != "foo" {
		t.Errorf("Expected 'foo', got '%s'", result1)
	}
	if result2 != "bar" {
		t.Errorf("Expected 'bar', got '%s'", result2)
	}
}

// Simulate 'find_meta' failure
func TestFindMetaFailure(t *testing.T) {
	content := ""
	findMeta := func(meta, content string) (string, error) {
		re := regexp.MustCompile(`__` + regexp.QuoteMeta(meta) + `__\s*=\s*['"]([^'"]*)['"]`)
		match := re.FindStringSubmatch(content)
		if len(match) > 1 {
			return match[1], nil
		}
		return "", errors.New("Unable to find __" + meta + "__ string.")
	}
	_, err := findMeta("whatever", content)
	if err == nil {
		t.Fatalf("Expected error for missing meta, got nil")
	}
}