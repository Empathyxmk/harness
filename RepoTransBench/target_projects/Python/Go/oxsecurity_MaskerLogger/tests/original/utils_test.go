package original

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func getConfigFilePath(filename ...string) string {
	// Stubbed for translation: Simulate same logic as Python `utils.get_config_file_path`
	// - If no filename, use "gitleaks.toml"
	// - Return path with "config" folder
	cwd, _ := os.Getwd()
	config := "gitleaks.toml"
	if len(filename) > 0 {
		config = filename[0]
	}
	return filepath.Join(cwd, "maskerlogger", "config", config)
}

func TestGetConfigFilePath(t *testing.T) {
	path := getConfigFilePath()
	if !strings.HasSuffix(path, "gitleaks.toml") {
		t.Errorf("Path should end with gitleaks.toml, got: %v", path)
	}
	if !strings.Contains(path, "config") {
		t.Errorf("Path should contain config folder, got: %v", path)
	}
}

func TestGetConfigFilePathCustom(t *testing.T) {
	cfg := getConfigFilePath("customfile.toml")
	if !strings.HasSuffix(cfg, "customfile.toml") {
		t.Errorf("Should end with customfile.toml, got: %v", cfg)
	}
}