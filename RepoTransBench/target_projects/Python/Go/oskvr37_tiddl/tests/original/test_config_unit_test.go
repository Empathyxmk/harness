package original

import (
	"os"
	"testing"
)

type DummyConfig struct {
	APIKey string
	Path   string
	Loaded bool
}

func LoadDummyConfig(path string) (*DummyConfig, error) {
	return &DummyConfig{
		APIKey: "testapikey123",
		Path:   path,
		Loaded: true,
	}, nil
}

func TestLoadDummyConfig(t *testing.T) {
	tmpfile := "config_test_dummy.json"
	f, err := os.Create(tmpfile)
	if err != nil {
		t.Fatalf("Could not create dummy config file: %v", err)
	}
	f.Close()
	cfg, err := LoadDummyConfig(tmpfile)
	if err != nil {
		t.Fatalf("Failed to load dummy config: %v", err)
	}
	if !cfg.Loaded {
		t.Errorf("Expected Loaded=true, got false")
	}
	if cfg.APIKey != "testapikey123" {
		t.Errorf("APIKey = %q, want \"testapikey123\"", cfg.APIKey)
	}
	_ = os.Remove(tmpfile)
}