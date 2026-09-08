package public_tests

import (
	"testing"
)

type DummyBuilder struct {
	config string
}

func (b *DummyBuilder) CustomConfig(config string) *DummyBuilder {
	b.config = config
	return b
}

func (b *DummyBuilder) GetConfig() string {
	return b.config
}

func TestSetsCustomConfigDifferentFromPrivateTest(t *testing.T) {
	builder := &DummyBuilder{}
	builder.CustomConfig("public_config_4567")
	if builder.GetConfig() != "public_config_4567" {
		t.Errorf("Expected config 'public_config_4567', got '%s'", builder.GetConfig())
	}
}

func TestConfigIsNullByDefault(t *testing.T) {
	builder := &DummyBuilder{}
	if builder.GetConfig() != "" {
		t.Errorf("Expected config to be empty by default, got '%s'", builder.GetConfig())
	}
}