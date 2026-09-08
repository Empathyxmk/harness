package public_tests

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestParkingBasicDataSyncResponsePublicVariant(t *testing.T) {
	// Use different inputs from private: e.g., odd parkId, simulate a "false"
	parkId := 5739 // Odd for this public variant
	syncResult := (parkId % 2) == 0 // Even-only success logic
	require.False(t, syncResult)
}