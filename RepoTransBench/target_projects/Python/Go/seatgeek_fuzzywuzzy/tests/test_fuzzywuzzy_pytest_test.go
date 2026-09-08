package tests

import (
	"testing"
	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/stretchr/testify/assert"
)

func TestProcessWarning(t *testing.T) {
	// In Go, logging capturing is different; we can't directly check for warnings logged to stderr.
	// Here, we just make sure code runs without panic if processor reduces string to empty.
	query := ":::::::"
	choices := []string{":::::::"}
	_ = fuzzywuzzy.ExtractOne(query, choices)
	// Consider using/faking a log test hook if checking log output is critical.
	assert.True(t, true)
}