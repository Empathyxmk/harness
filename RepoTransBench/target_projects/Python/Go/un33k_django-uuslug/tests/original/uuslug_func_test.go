package original

import (
	"testing"
)

func TestUuslugRaisesForModelBase(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected uuslug to panic on invalid input")
		}
	}()

	Uuslug("abc", struct{}{})
}

// Placeholder for the uuslug function.
func Uuslug(s string, inst interface{}) (string, error) {
	panic("not a model instance")
}