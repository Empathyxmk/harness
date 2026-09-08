package public_tests

import (
	"strings"
	"testing"
)

func TestGetConfigFilePathOtherCustom(t *testing.T) {
	cfg := getConfigFilePathPublic("anotherpublic.toml")
	if !strings.HasSuffix(cfg, "anotherpublic.toml") {
		t.Errorf("Path should end with anotherpublic.toml, got: %v", cfg)
	}
}

func TestGetConfigFilePathFolderCheck(t *testing.T) {
	cfg := getConfigFilePathPublic()
	ok := containsAny(cfg, "config")
	if !ok {
		t.Errorf("Path should contain 'config', got: %v", cfg)
	}
}

func containsAny(path string, s string) bool {
	parts := strings.Split(path, "/")
	for _, part := range parts {
		if part == s {
			return true
		}
	}
	parts = strings.Split(path, "\\")
	for _, part := range parts {
		if part == s {
			return true
		}
	}
	return false
}