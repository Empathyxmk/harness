package original

import (
	"path/filepath"
	"testing"
)

type Config struct {
	Path   string
	Runner string
	Delay  float64
}

func TestConfigWithMissingFile(t *testing.T) {
	conf := &Config{Path: filepath.Join("tmp", "notexisting.toml")}
	if conf.Path == "" {
		t.Error("Config.Path should exist")
	}
}

func TestConfigFallbackDefault(t *testing.T) {
	conf := &Config{Path: filepath.Join("tmp", "notexisting2.toml"), Runner: "pytest", Delay: 0.2}
	if conf.Path != filepath.Join("tmp", "notexisting2.toml") {
		t.Errorf("Config.Path incorrect, got %v", conf.Path)
	}
	if conf.Runner != "pytest" {
		t.Errorf("Default runner should be pytest")
	}
	if conf.Delay != 0.2 {
		t.Errorf("Default delay should be 0.2")
	}
}