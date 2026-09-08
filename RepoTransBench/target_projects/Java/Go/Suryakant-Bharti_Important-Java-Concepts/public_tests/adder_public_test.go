package public_tests

import (
	"math"
	"testing"
)

func TestAdderAddIntPublic(t *testing.T) {
	if got := Add(9, 8); got != 17 {
		t.Errorf("Add(9, 8) = %d; want 17", got)
	}
	if got := Add(15, 10); got != 25 {
		t.Errorf("Add(15, 10) = %d; want 25", got)
	}
	if got := Add(-3, -3); got != -6 {
		t.Errorf("Add(-3, -3) = %d; want -6", got)
	}
}

func TestAdderAddFloatPublic(t *testing.T) {
	if got := AddFloat(9.5, 11.6); math.Abs(got-21.1) > 1e-9 {
		t.Errorf("AddFloat(9.5, 11.6) = %f; want 21.1", got)
	}
	if got := AddFloat(-7.7, 7.7); math.Abs(got-0.0) > 1e-9 {
		t.Errorf("AddFloat(-7.7, 7.7) = %f; want 0.0", got)
	}
	if got := AddFloat(-2.2, -4.4); math.Abs(got+6.6) > 1e-9 {
		t.Errorf("AddFloat(-2.2, -4.4) = %f; want -6.6", got)
	}
}