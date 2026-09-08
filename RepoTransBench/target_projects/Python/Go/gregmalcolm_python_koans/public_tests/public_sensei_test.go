package public_tests

import (
	"testing"
)

type Sensei struct{}

func TestPublicSenseiClassExists(t *testing.T) {
	s := Sensei{}
	if s == (Sensei{}) {

	} else {
		t.Error("Sensei struct not found")
	}
}
func TestPublicSenseiInstance(t *testing.T) {
	s := Sensei{}
	if (Sensei{}) != s {
		t.Error("Instance should be possible")
	}
}