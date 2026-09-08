package public_tests

import (
	"strings"
	"testing"
)

func getConfigFilePathPublic(filename ...string) string {
	// Simulates utils.get_config_file_path in a public test context
	name := "gitleaks.toml"
	if len(filename) > 0 {
		name = filename[0]
	}
	// Example path
	return "/tmp/maskerlogger/config/" + name
}

func TestGetConfigFilePathNonDefault(t *testing.T) {
	path := getConfigFilePathPublic("alternative_config.toml")
	if !strings.HasSuffix(path, "alternative_config.toml") {
		t.Errorf("Should end with alternative_config.toml, got: %s", path)
	}
}

func TestGetConfigFilePathContainsMaskerlogger(t *testing.T) {
	path := getConfigFilePathPublic()
	if !strings.Contains(path, "maskerlogger") {
		t.Errorf("Should contain 'maskerlogger' in path, got: %s", path)
	}
}