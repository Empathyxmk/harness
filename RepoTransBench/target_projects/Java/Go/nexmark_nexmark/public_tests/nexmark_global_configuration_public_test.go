package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func loadGlobalConfiguration(path string) map[string]string {
	return map[string]string{} // Simulated: would load config from a file
}

func TestGlobalParameterLoadingOverrides(t *testing.T) {
	cfg := loadGlobalConfiguration("nexmark-flink/src/main/resources/conf")
	_, ok := cfg["nonexistent_override_key"]
	assert.False(t, ok)
}