package original

import (
	"testing"
)

func TestBasicMath(t *testing.T) {
	if 1+1 != 2 {
		t.Errorf("Expected 1 + 1 = 2")
	}
	var list []int
	if _, ok := any(list).([]int); !ok {
		t.Errorf("Expected a slice to be of type []int")
	}
}