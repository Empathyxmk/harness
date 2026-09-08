package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate NewsfeedConfig and registry
type NewsfeedConfig struct{}
type AppConfig struct{ Name string }

func (NewsfeedConfig) Name() string { return "newsfeed" }

func getAppConfig(name string) *AppConfig {
	return &AppConfig{Name: name}
}

func TestNewsfeedConfig_Apps(t *testing.T) {
	assert.Equal(t, "newsfeed", NewsfeedConfig{}.Name())
	assert.Equal(t, "newsfeed", getAppConfig("newsfeed").Name)
}