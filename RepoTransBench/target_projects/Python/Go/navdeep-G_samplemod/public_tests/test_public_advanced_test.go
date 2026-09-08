package public_tests

import (
	"testing"

	"navdeepG_samplemod/sample"
)

func TestSafeDivideNormalPublic(t *testing.T) {
	if got := sample.SafeDivide(15, 3); got != 5 {
		t.Errorf("SafeDivide(15, 3) = %d, want 5", got)
	}
}

func TestSafeDivideNegativePublic(t *testing.T) {
	if got := sample.SafeDivide(-9, 3); got != -3 {
		t.Errorf("SafeDivide(-9, 3) = %d, want -3", got)
	}
}

func TestSafeDivideZeroDividendPublic(t *testing.T) {
	if got := sample.SafeDivide(0, 2); got != 0 {
		t.Errorf("SafeDivide(0, 2) = %d, want 0", got)
	}
}

func TestSafeDivideRaisesZeroDivisionPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("SafeDivide(2, 0) did not panic, want division by zero panic")
		}
	}()
	_ = sample.SafeDivide(2, 0)
}