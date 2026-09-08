package public_tests

import (
	"testing"
)

func TestBasicMathPublic(t *testing.T) {
	if 2*3 != 6 {
		t.Errorf("Expected 2 * 3 = 6")
	}
	var m map[string]int
	if _, ok := any(m).(map[string]int); !ok {
		t.Errorf("Expected a map to be of type map[string]int")
	}
}