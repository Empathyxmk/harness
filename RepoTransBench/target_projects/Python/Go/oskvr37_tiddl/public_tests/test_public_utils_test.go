package public

import (
	"testing"
)

func IsEven(n int) bool {
	return n%2 == 0
}

func TestIsEven(t *testing.T) {
	if !IsEven(4) {
		t.Errorf("IsEven(4) = false, want true")
	}
	if IsEven(5) {
		t.Errorf("IsEven(5) = true, want false")
	}
	if !IsEven(0) {
		t.Errorf("IsEven(0) = false, want true")
	}
}