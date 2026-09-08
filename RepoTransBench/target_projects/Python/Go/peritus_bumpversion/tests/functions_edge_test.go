package tests

import (
	"testing"
	"bumpversion/functions"
)

func TestNumericFunctionBasicBump(t *testing.T) {
	nf := functions.NewNumericFunction("3")
	if nf.Bump("3") != "4" {
		t.Errorf("Expected bump('3') = '4', got '%v'", nf.Bump("3"))
	}
	if nf.Bump("99") != "100" {
		t.Errorf("Expected bump('99') = '100', got '%v'", nf.Bump("99"))
	}
}

func TestNumericFunctionFirstValueAndOptionalValue(t *testing.T) {
	nf := functions.NewNumericFunction("00")
	if nf.FirstValue() != "00" {
		t.Errorf("Expected first_value = '00', got '%v'", nf.FirstValue())
	}
	if nf.OptionalValue() != "00" {
		t.Errorf("Expected optional_value = '00', got '%v'", nf.OptionalValue())
	}
}

func TestNumericFunctionAlphanumeric(t *testing.T) {
	nf := functions.NewNumericFunction("r3")
	if nf.Bump("r3") != "r4" {
		t.Errorf("Expected bump('r3') = 'r4', got '%v'", nf.Bump("r3"))
	}
	nf2 := functions.NewNumericFunction("r3-001")
	if nf2.Bump("r3-001") != "r4-001" {
		t.Errorf("Expected bump('r3-001') = 'r4-001', got '%v'", nf2.Bump("r3-001"))
	}
}

func TestNumericFunctionInvalidFirstValue(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected ValueError for invalid first value")
		}
	}()
	_ = functions.NewNumericFunction("abc")
}

func TestNumericFunctionNoDigits(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected error when no digit is in value")
		}
	}()
	n := functions.NewNumericFunction("")
	_ = n.Bump("abc")
}

func TestValuesFunctionBumpAndErrors(t *testing.T) {
	vf, err := functions.NewValuesFunction([]string{"alpha", "beta", "rc", "final"}, "alpha", "alpha")
	if err != nil {
		t.Fatalf("Init error: %v", err)
	}
	if v, err := vf.BumpVal("alpha"); v != "beta" || err != nil {
		t.Errorf("Expected bump('alpha') = 'beta', got %v, %v", v, err)
	}
	if v, err := vf.BumpVal("beta"); v != "rc" || err != nil {
		t.Errorf("Expected bump('beta') = 'rc', got %v, %v", v, err)
	}
	if v, err := vf.BumpVal("rc"); v != "final" || err != nil {
		t.Errorf("Expected bump('rc') = 'final', got %v, %v", v, err)
	}
	_, err = vf.BumpVal("final")
	if err == nil {
		t.Errorf("Expected error for bumping final value")
	}
}

func TestValuesFunctionInvalidEmpty(t *testing.T) {
	_, err := functions.NewValuesFunction([]string{}, "", "")
	if err == nil {
		t.Errorf("Expected ValueError for empty values")
	}
}

func TestValuesFunctionOptionalValueNotInValues(t *testing.T) {
	_, err := functions.NewValuesFunction([]string{"a", "b"}, "c", "a")
	if err == nil {
		t.Errorf("Expected ValueError for optional_value not in values")
	}
}

func TestValuesFunctionFirstValueNotInValues(t *testing.T) {
	_, err := functions.NewValuesFunction([]string{"a", "b"}, "a", "c")
	if err == nil {
		t.Errorf("Expected ValueError for first_value not in values")
	}
}