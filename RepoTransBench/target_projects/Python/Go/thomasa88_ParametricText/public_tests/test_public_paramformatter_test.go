package public_tests

import (
	"testing"
	"fmt"
)

type Param struct {
	Value float64
	Unit  string
}

func makeParam(val float64, unit string) Param {
	return Param{Value: val, Unit: unit}
}

// Simple Go translation of mixed_frac_inch for public tests (no " for unitless)
func mixedFracInch(p Param, _ interface{}) string {
	val := p.Value

	neg := false
	if val < 0 {
		neg = true
		val = -val
	}
	whole := int(val)
	frac := val - float64(whole)
	type fracT struct{ v float64; s string }
	fractions := []fracT{
		{0.0, ""},
		{0.125, "1/8"},
		{0.25, "1/4"},
		{0.375, "3/8"},
		{0.5, "1/2"},
		{0.625, "5/8"},
		{0.75, "3/4"},
		{0.875, "7/8"},
	}
	closeVal := 0.0
	closeStr := ""
	for _, f := range fractions {
		if abs(frac-f.v) < 0.0625 {
			closeVal = f.v
			closeStr = f.s
			break
		}
	}
	frac = closeVal
	sign := ""
	if neg {
		sign = "-"
	}
	switch {
	case whole == 0 && frac == 0:
		return "0"
	case whole == 0:
		return fmt.Sprintf("%s%s", sign, closeStr)
	case frac == 0:
		return fmt.Sprintf("%s%d", sign, whole)
	default:
		return fmt.Sprintf("%s%d %s", sign, whole, closeStr)
	}
}

func abs(a float64) float64 {
	if a < 0 { return -a }
	return a
}

func TestMixedFracInchWholeNumber(t *testing.T) {
	p := makeParam(15, "")
	if got := mixedFracInch(p, nil); got != "15" {
		t.Errorf("Expected 15, got %q", got)
	}
}
func TestMixedFracInchSimpleFraction(t *testing.T) {
	p := makeParam(0.625, "")
	if got := mixedFracInch(p, nil); got != "5/8" {
		t.Errorf("Expected 5/8, got %q", got)
	}
}
func TestMixedFracInchMixed(t *testing.T) {
	p := makeParam(3.75, "")
	if got := mixedFracInch(p, nil); got != "3 3/4" {
		t.Errorf("Expected 3 3/4, got %q", got)
	}
}
func TestMixedFracInchExactHalf(t *testing.T) {
	p := makeParam(6.5, "")
	if got := mixedFracInch(p, nil); got != "6 1/2" {
		t.Errorf("Expected 6 1/2, got %q", got)
	}
}
func TestMixedFracInchZero(t *testing.T) {
	p := makeParam(0, "")
	if got := mixedFracInch(p, nil); got != "0" {
		t.Errorf("Expected 0, got %q", got)
	}
}