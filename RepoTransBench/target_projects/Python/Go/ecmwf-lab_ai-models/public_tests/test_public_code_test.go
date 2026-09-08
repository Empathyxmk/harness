package public_tests

import (
	"math"
	"testing"
)

func TestPublicCodeMathOps(t *testing.T) {
	x, y := 3, 9
	if x*y != 27 {
		t.Errorf("(x*y) = %d, want 27", x*y)
	}
	if math.Pow(float64(y), 0.5) != 3 {
		t.Errorf("pow(y, 1/2) = %f, want 3", math.Pow(float64(y), 0.5))
	}
}

func TestPublicCodeStringReverse(t *testing.T) {
	s := "abcdef"
	rev := reverse(s)
	if rev != "fedcba" {
		t.Errorf("reverse(%v) = %v, want fedcba", s, rev)
	}
}

// Helper
func reverse(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}