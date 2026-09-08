package original

import (
	"testing"

	"kevinburke_hamms/hamms"
)

func TestMorseDummy(t *testing.T) {
	// Dummy test, always true.
	_ = hamms.Morse
	if true != true {
		t.Errorf("True is not true")
	}
}