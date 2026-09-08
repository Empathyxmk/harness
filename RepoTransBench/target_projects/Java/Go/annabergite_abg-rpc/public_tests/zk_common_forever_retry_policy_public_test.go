package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ForeverRetryPolicy struct{}

func (f *ForeverRetryPolicy) ShouldRetry(attempt int) bool {
	return true
}

func TestShouldRetryAfterDifferentAttempt(t *testing.T) {
	attempt := 42
	policy := &ForeverRetryPolicy{}
	shouldRetry := policy.ShouldRetry(attempt)
	assert.True(t, shouldRetry, "Should always retry regardless of attempt (public test)")
}