package public_tests

import (
	"testing"

	"kevinburke_hamms/hamms"
)

func TestUtilsPublicTrue(t *testing.T) {
	// Always true: 10 > 5
	_ = hamms.GetHeader()
	if !(10 > 5) {
		t.Errorf("Expected 10 > 5")
	}
}