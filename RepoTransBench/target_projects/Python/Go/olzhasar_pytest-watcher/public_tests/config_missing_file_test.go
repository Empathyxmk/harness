package public_tests

import (
	"errors"
	"path/filepath"
	"testing"
)

type Config struct {
	Path string
}

func (conf *Config) Load() error {
	// Simulate error when loading non-existent file
	return errors.New("file not found")
}

func TestConfigFileNotExistent(t *testing.T) {
	conf := &Config{Path: filepath.Join("surely_nonexistent_toml.toml")}
	if conf.Path == "" {
		t.Error("Config.Path name not set")
	}
	// Trying to load should raise error
	if err := conf.Load(); err == nil {
		t.Error("Expected error when loading non-existent file")
	}
}