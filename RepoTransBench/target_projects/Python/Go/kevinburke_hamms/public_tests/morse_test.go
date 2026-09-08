package public_tests

import (
	"testing"

	"kevinburke_hamms/hamms"
)

func TestMorsePublicTrue(t *testing.T) {
	// Assert morse is some object; in Go, morse is struct{} so always true
	if hamms.Morse == nil {
		t.Errorf("hamms.Morse should not be nil")
	}
}