package original

import (
	"testing"
)

func Increment(a int) int {
	return a + 1
}

func TestIncrement(t *testing.T) {
	if Increment(4) != 5 {
		t.Errorf("Increment(4) = %d, want 5", Increment(4))
	}
	if Increment(-1) != 0 {
		t.Errorf("Increment(-1) = %d, want 0", Increment(-1))
	}
}