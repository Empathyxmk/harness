package public_tests

import (
	"testing"
)

func TestExampleInstrumentedPublic(t *testing.T) {
	actual := 1 + 1
	expected := 2
	if actual != expected {
		t.Errorf("Expected %d but got %d", expected, actual)
	}
}