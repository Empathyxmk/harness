package original

import (
	"testing"

	"kevinburke_hamms/hamms"
)

func TestDummyServerStart(t *testing.T) {
	_ = hamms.HammsServer{}
	_ = hamms.Reactor
	if true != true {
		t.Errorf("True is not true")
	}
}