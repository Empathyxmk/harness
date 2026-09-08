package public

import (
	"testing"
)

func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func TestMin(t *testing.T) {
	if Min(3, 5) != 3 {
		t.Errorf("Min(3,5) = %d, want 3", Min(3, 5))
	}
	if Min(5, 3) != 3 {
		t.Errorf("Min(5,3) = %d, want 3", Min(5, 3))
	}
	if Min(5, 5) != 5 {
		t.Errorf("Min(5,5) = %d, want 5", Min(5, 5))
	}
}