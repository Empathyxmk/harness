package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func unknownKwargs(kwargs map[string]interface{}) map[string]interface{} {
	return kwargs
}

func TestUnknownKwargsGetsFiltered(t *testing.T) {
	result := unknownKwargs(map[string]interface{}{
		"alpha":  "beta",
		"gamma":  42,
		"is_test": true,
	})
	assert.Equal(t, map[string]interface{}{
		"alpha":  "beta",
		"gamma":  42,
		"is_test": true,
	}, result)
}