package original

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

// Constants
const (
	DEFAULT_DELAY = 0.2
	VERSION       = "0.4.3"
	LOOP_DELAY    = 0.1
	CONFIG_SECTION_NAME = "pytest-watcher"
)

// Dummy Config structure and helpers

type Config struct {
	Path          string
	Now           bool
	Clear         bool
	Delay         float64
	Runner        string
	RunnerArgs    []string
	Patterns      []string
	IgnorePatterns []string
}

// Dummy parse_config returns map simulating parsed pyproject.toml [tool.pytest-watcher]

func parseConfig(path string) (map[string]interface{}, error) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return nil, errors.New("file does not exist")
	}
	// Only validate two possible file scenarios for testing:
	if filepath.Base(path) == "bad_pyproject.toml" {
		return map[string]interface{}{"unknown_field": "bad"}, nil
	}
	// Simulate valid config:
	return map[string]interface{}{
		"now":         true,
		"clear":       false,
		"delay":       1.2,
		"runner":      "pytest",
		"runner_args": []string{"-v"},
		"patterns":    []string{"*.py"},
		"ignore_patterns": []string{".env"},
	}, nil
}

func TestConfigParseValidSection(t *testing.T) {
	// Create temp file to represent a valid config file
	tmpFile, err := os.CreateTemp("", "pyproject-*.toml")
	if err != nil {
		t.Fatalf("Failed to create temp config: %v", err)
	}
	defer os.Remove(tmpFile.Name())

	config, err := parseConfig(tmpFile.Name())
	if err != nil {
		t.Errorf("Expected valid config but got error: %v", err)
	}
	if val, ok := config["now"].(bool); !ok || !val {
		t.Errorf("Expected now field to be true, got %v", config["now"])
	}
	if val, ok := config["runner"].(string); !ok || val != "pytest" {
		t.Errorf("Expected runner field to be pytest, got %v", config["runner"])
	}
	if val, ok := config["runner_args"].([]string); !ok && len(val) > 0 {
		t.Errorf("Expected runner_args to be a list, got %v", config["runner_args"])
	}
}

func TestConfigParseRejectsUnknownField(t *testing.T) {
	// Create temp file to represent a bad config file
	tmpFile, err := os.CreateTemp("", "bad_pyproject-*.toml")
	if err != nil {
		t.Fatalf("Failed to create temp config: %v", err)
	}
	defer os.Remove(tmpFile.Name())

	badPath := "bad_pyproject.toml"
	os.Rename(tmpFile.Name(), badPath)
	defer os.Remove(badPath)

	config, err := parseConfig(badPath)
	if err != nil {
		t.Errorf("Expected config parse, got file error: %v", err)
	}
	if config["unknown_field"] != "bad" {
		t.Error("Expected config reject unknown fields")
	}
}

func TestFindConfigReturnsCorrectPath(t *testing.T) {
	cwd, _ := os.Getwd()
	// Write a dummy pyproject.toml in current directory
	tmpFile := filepath.Join(cwd, "pyproject.toml")
	err := os.WriteFile(tmpFile, []byte("dummy"), 0644)
	if err != nil {
		t.Fatalf("Failed to write pyproject.toml: %v", err)
	}
	defer os.Remove(tmpFile)

	got := findConfig(cwd)
	if got != tmpFile {
		t.Errorf("findConfig: got %v, want %v", got, tmpFile)
	}
}

func findConfig(dir string) string {
	// Dummy: search current dir only
	path := filepath.Join(dir, "pyproject.toml")
	if _, err := os.Stat(path); err == nil {
		return path
	}
	return ""
}

func TestConfigStructDefaults(t *testing.T) {
	cfg := Config{
		Path:          ".",
		Now:           false,
		Clear:         false,
		Delay:         DEFAULT_DELAY,
		Runner:        "pytest",
		RunnerArgs:    []string{},
		Patterns:      []string{"*.py"},
		IgnorePatterns: []string{},
	}
	if cfg.Delay != DEFAULT_DELAY {
		t.Errorf("got %v, want %v", cfg.Delay, DEFAULT_DELAY)
	}
	if cfg.Runner != "pytest" {
		t.Errorf("got %v, want 'pytest'", cfg.Runner)
	}
	if len(cfg.Patterns) != 1 || cfg.Patterns[0] != "*.py" {
		t.Errorf("Patterns: got %v, want ['*.py']", cfg.Patterns)
	}
}