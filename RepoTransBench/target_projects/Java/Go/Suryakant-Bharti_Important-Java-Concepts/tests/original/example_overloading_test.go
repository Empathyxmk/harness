package original

import (
	"math"
	"testing"
)

func TestMinFunctionInt(t *testing.T) {
	if got := MinFunction(11, 6); got != 6 {
		t.Errorf("MinFunction(11, 6) = %d; want 6", got)
	}
	if got := MinFunction(-3, 4); got != -3 {
		t.Errorf("MinFunction(-3, 4) = %d; want -3", got)
	}
	if got := MinFunction(-5, -2); got != -5 {
		t.Errorf("MinFunction(-5, -2) = %d; want -5", got)
	}
	if got := MinFunction(7, 7); got != 7 {
		t.Errorf("MinFunction(7, 7) = %d; want 7", got)
	}
}

func TestMinFunctionFloat(t *testing.T) {
	if got := MinFunctionFloat(7.3, 9.4); math.Abs(got-7.3) > 1e-9 {
		t.Errorf("MinFunctionFloat(7.3, 9.4) = %f; want 7.3", got)
	}
	if got := MinFunctionFloat(-5.5, 0.0); math.Abs(got+5.5) > 1e-9 {
		t.Errorf("MinFunctionFloat(-5.5, 0.0) = %f; want -5.5", got)
	}
	if got := MinFunctionFloat(-10.2, -2.3); math.Abs(got+10.2) > 1e-9 {
		t.Errorf("MinFunctionFloat(-10.2, -2.3) = %f; want -10.2", got)
	}
	if got := MinFunctionFloat(12.0, 12.0); math.Abs(got-12.0) > 1e-9 {
		t.Errorf("MinFunctionFloat(12.0, 12.0) = %f; want 12.0", got)
	}
}