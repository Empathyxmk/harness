package unit

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
	"regexp"
	"errors"
)

func readFilePublic(paths ...string) (string, error) {
	fullPath := filepath.Join(paths...)
	data, err := ioutil.ReadFile(fullPath)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func TestReadReadsFilePublic(t *testing.T) {
	dir := t.TempDir()
	pkgDir := filepath.Join(dir, "flask_redis")
	err := os.Mkdir(pkgDir, 0o755)
	if err != nil && !os.IsExist(err) {
		t.Fatalf("Failed to create directory: %v", err)
	}
	filePath := filepath.Join(pkgDir, "testfile_public.txt")
	testText := "123xyz"
	if err := ioutil.WriteFile(filePath, []byte(testText), 0644); err != nil {
		t.Fatalf("Failed to write file: %v", err)
	}
	result, err := readFilePublic(filePath)
	if err != nil {
		t.Fatalf("Failed to read via readFilePublic: %v", err)
	}
	if result != testText {
		t.Errorf("Expected '%s', got '%s'", testText, result)
	}
}

func TestFindMetaSuccessPublic(t *testing.T) {
	content := "__spam__ = 'eggs'\n__hamp__ = 'bacon'"
	findMeta := func(meta, content string) (string, error) {
		re := regexp.MustCompile(`__` + regexp.QuoteMeta(meta) + `__\s*=\s*['"]([^'"]*)['"]`)
		match := re.FindStringSubmatch(content)
		if len(match) > 1 {
			return match[1], nil
		}
		return "", errors.New("Unable to find __" + meta + "__ string.")
	}
	result1, err1 := findMeta("spam", content)
	if err1 != nil {
		t.Fatalf("Expected to find 'spam': %v", err1)
	}
	result2, err2 := findMeta("hamp", content)
	if err2 != nil {
		t.Fatalf("Expected to find 'hamp': %v", err2)
	}
	if result1 != "eggs" {
		t.Errorf("Expected 'eggs', got '%s'", result1)
	}
	if result2 != "bacon" {
		t.Errorf("Expected 'bacon', got '%s'", result2)
	}
}

func TestFindMetaFailurePublic(t *testing.T) {
	content := ""
	findMeta := func(meta, content string) (string, error) {
		re := regexp.MustCompile(`__` + regexp.QuoteMeta(meta) + `__\s*=\s*['"]([^'"]*)['"]`)
		match := re.FindStringSubmatch(content)
		if len(match) > 1 {
			return match[1], nil
		}
		return "", errors.New("Unable to find __" + meta + "__ string.")
	}
	_, err := findMeta("somethingelse", content)
	if err == nil {
		t.Fatalf("Expected error for missing meta, got nil")
	}
}