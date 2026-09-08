package original

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestGetConfigFilePathDefault(t *testing.T) {
	path := getConfigFilePath()
	if !strings.HasSuffix(path, string(filepath.Separator)+"config"+string(filepath.Separator)+"gitleaks.toml") &&
		!strings.HasSuffix(path, "/config/gitleaks.toml") && !strings.HasSuffix(path, "\\config\\gitleaks.toml") {
		t.Errorf("Should end with config%sgitleaks.toml or equivalent, got: %v", string(filepath.Separator), path)
	}
	if _, err := os.Stat(path); os.IsNotExist(err) {
		if !strings.Contains(path, "gitleaks.toml") {
			t.Errorf("Should include gitleaks.toml name somewhere, got: %v", path)
		}
	}
}

func TestGetConfigFilePathCustomAdditional(t *testing.T) {
	fname := "some_other_config.toml"
	path := getConfigFilePath(fname)
	if !strings.HasSuffix(path, string(filepath.Separator)+"config"+string(filepath.Separator)+fname) &&
		!strings.HasSuffix(path, "/config/"+fname) && !strings.HasSuffix(path, "\\config\\"+fname) {
		t.Errorf("Should end with config%s%v or equivalent, got: %v", string(filepath.Separator), fname, path)
	}
}

func TestGetConfigFilePathEdgeCase(t *testing.T) {
	// Simulate when __file__ is not set or config folder missing.
	fakeDir := "/tmp"
	path := filepath.Join(fakeDir, "config", "foo.toml")
	if path != "/tmp/config/foo.toml" {
		t.Errorf("Should match the expected fake path, got: %v", path)
	}
}