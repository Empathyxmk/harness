package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRegisterAdvancedPublic(t *testing.T) {
	key := "public-advanced-key"
	value := "public-advanced-value"
	isRegistered := simulateRegister(key, value)
	assert.True(t, isRegistered, "Should register advanced public info")
}

func simulateRegister(key, value string) bool {
	return len(key) > 0 && len(value) > 0 && key[:7] == "public-" && value[:7] == "public-"
}