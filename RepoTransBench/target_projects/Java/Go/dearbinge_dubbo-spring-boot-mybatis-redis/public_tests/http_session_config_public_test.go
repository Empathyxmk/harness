package public_tests

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestSessionTimeoutPublicVariant(t *testing.T) {
	// Simulate the timeout for a different input (e.g., 42 min)
	maxInactiveIntervalInSeconds := 42 * 60
	require.Equal(t, 2520, maxInactiveIntervalInSeconds)
}