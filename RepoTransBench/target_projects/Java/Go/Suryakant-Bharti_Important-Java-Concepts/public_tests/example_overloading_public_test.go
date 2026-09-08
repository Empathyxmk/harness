package public_tests

import (
	"math"
	"testing"
)

func TestMinFunctionIntPublic(t *testing.T) {
	if got := MinFunction(5, 2); got != 2 {
		t.Errorf("MinFunction(5, 2) = %d; want 2", got)
	}
	if got := MinFunction(-7, 9); got != -7 {
		t.Errorf("MinFunction(-7, 9) = %d; want -7", got)
	}
	if got := MinFunction(-15, -20); got != -20 {
		t.Errorf("MinFunction(-15, -20) = %d; want -20", got)
	}
	if got := MinFunction(0, 0); got != 0 {
		t.Errorf("MinFunction(0, 0) = %d; want 0", got)
	}
}

func TestMinFunctionFloatPublic(t *testing.T) {
	if got := MinFunctionFloat(8.7, 3.2); math.Abs(got-3.2) > 1e-9 {
		t.Errorf("MinFunctionFloat(8.7, 3.2) = %f; want 3.2", got)
	}
	if got := MinFunctionFloat(-9.8, 4.5); math.Abs(got+9.8) > 1e-9 {
		t.Errorf("MinFunctionFloat(-9.8, 4.5) = %f; want -9.8", got)
	}
	if got := MinFunctionFloat(-11.3, -6.5); math.Abs(got+11.3) > 1e-9 {
		t.Errorf("MinFunctionFloat(-11.3, -6.5) = %f; want -11.3", got)
	}
	if got := MinFunctionFloat(-7.7, -7.7); math.Abs(got+7.7) > 1e-9 {
		t.Errorf("MinFunctionFloat(-7.7, -7.7) = %f; want -7.7", got)
	}
}