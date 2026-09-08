package original

import (
	"math"
	"testing"
)

func TestAdderAddInt(t *testing.T) {
	if got := Add(11, 11); got != 22 {
		t.Errorf("Add(11, 11) = %d; want 22", got)
	}
	if got := Add(-10, 2); got != -8 {
		t.Errorf("Add(-10, 2) = %d; want -8", got)
	}
	if got := Add(0, 0); got != 0 {
		t.Errorf("Add(0, 0) = %d; want 0", got)
	}
}

func TestAdderAddFloat(t *testing.T) {
	if got := AddFloat(12.3, 12.6); math.Abs(got-24.9) > 1e-9 {
		t.Errorf("AddFloat(12.3, 12.6) = %f; want 24.9", got)
	}
	if got := AddFloat(-2.2, -2.2); math.Abs(got+4.4) > 1e-9 {
		t.Errorf("AddFloat(-2.2, -2.2) = %f; want -4.4", got)
	}
	if got := AddFloat(0.0, 0.0); math.Abs(got-0.0) > 1e-9 {
		t.Errorf("AddFloat(0.0, 0.0) = %f; want 0.0", got)
	}
}

// The Add/Adder function implementations, to be placed in module.go or testutil.go if needed.