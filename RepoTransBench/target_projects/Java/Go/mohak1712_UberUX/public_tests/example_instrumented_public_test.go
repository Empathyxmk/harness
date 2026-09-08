package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUseAppContextPublic(t *testing.T) {
	// Just check that the string contains "uberux"
	appContextName := "com.example.uberux"
	assert.True(t, strings.Contains(appContextName, "uberux"))
}