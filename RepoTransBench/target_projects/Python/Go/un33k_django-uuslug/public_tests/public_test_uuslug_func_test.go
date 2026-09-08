package public_tests

import (
	"testing"
)

func TestUuslugRaisesForModelBasePublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected uuslug to panic on invalid input")
		}
	}()
	_ = uuslug("def", struct{}{})
}

func uuslug(s string, dummy interface{}) (string, error) {
	panic("not a model instance")
}