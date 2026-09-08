package original

import (
	"testing"

	"kevinburke_hamms/hamms"
)

func TestUtilsDummy(t *testing.T) {
	// Dummy test, always true.
	_ = hamms.GetHeader()
	if true != true {
		t.Errorf("True is not true")
	}
}