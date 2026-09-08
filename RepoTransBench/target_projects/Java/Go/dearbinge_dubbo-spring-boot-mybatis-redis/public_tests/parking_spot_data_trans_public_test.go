package public_tests

import (
	"math"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestAlternativeParkingSpotTrans(t *testing.T) {
	// Different inputs from private: new spotId, different lat/lng.
	spotId := "PUBLIC_SPOT_102"
	lat := 35.1234
	lng := 135.4321

	// Simulate test logic
	result := spotId + "_" + strings.TrimRight(strings.TrimRight(
		strconv.FormatFloat(math.Abs(lat-lng), 'f', 4, 64), "0"), ".")
	require.Equal(t, "PUBLIC_SPOT_102_100.3087", result)
}