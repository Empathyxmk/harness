package tests

import (
	"testing"
	"bumpversion/functions"
)

func TestNumericInitWithoutFirstValue(t *testing.T) {
	funcObj := functions.NewNumericFunction("")
	if funcObj.FirstValue() != "0" {
		t.Errorf("Expected first_value to be '0', got '%v'", funcObj.FirstValue())
	}
}

func TestNumericInitWithFirstValue(t *testing.T) {
	funcObj := functions.NewNumericFunction("5")
	if funcObj.FirstValue() != "5" {
		t.Errorf("Expected first_value to be '5', got '%v'", funcObj.FirstValue())
	}
}

func TestNumericInitNonNumericFirstValue(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected ValueError for non-numeric first_value")
		}
	}()
	_ = functions.NewNumericFunction("a")
}

func TestNumericBumpSimpleNumber(t *testing.T) {
	funcObj := functions.NewNumericFunction("")
	if bumped := funcObj.Bump("0"); bumped != "1" {
		t.Errorf("Expected bump('0') = '1', got '%v'", bumped)
	}
}

func TestNumericBumpPrefixAndSuffix(t *testing.T) {
	funcObj := functions.NewNumericFunction("")
	if bumped := funcObj.Bump("v0b"); bumped != "v1b" {
		t.Errorf("Expected bump('v0b') = 'v1b', got '%v'", bumped)
	}
}

func TestValuesInit(t *testing.T) {
	funcObj, err := functions.NewValuesFunction([]int{0, 1, 2}, 0, 0)
	if err != nil {
		t.Fatalf("Init error: %v", err)
	}
	if funcObj.OptionalValue() != 0 {
		t.Errorf("Expected optional_value = 0")
	}
	if funcObj.FirstValue() != 0 {
		t.Errorf("Expected first_value = 0")
	}
}

func TestValuesInitWithCorrectOptionalValue(t *testing.T) {
	funcObj, err := functions.NewValuesFunction([]int{0, 1, 2}, 1, 0)
	if err != nil {
		t.Fatalf("Init error: %v", err)
	}
	if funcObj.OptionalValue() != 1 {
		t.Errorf("Expected optional_value = 1")
	}
	if funcObj.FirstValue() != 0 {
		t.Errorf("Expected first_value = 0")
	}
}

func TestValuesInitWithCorrectFirstValue(t *testing.T) {
	funcObj, err := functions.NewValuesFunction([]int{0, 1, 2}, 0, 1)
	if err != nil {
		t.Fatalf("Init error: %v", err)
	}
	if funcObj.OptionalValue() != 0 {
		t.Errorf("Expected optional_value = 0")
	}
	if funcObj.FirstValue() != 1 {
		t.Errorf("Expected first_value = 1")
	}
}

func TestValuesInitWithCorrectOptionalAndFirstValue(t *testing.T) {
	funcObj, err := functions.NewValuesFunction([]int{0, 1, 2}, 0, 1)
	if err != nil {
		t.Fatalf("Init error: %v", err)
	}
	if funcObj.OptionalValue() != 0 {
		t.Errorf("Expected optional_value = 0")
	}
	if funcObj.FirstValue() != 1 {
		t.Errorf("Expected first_value = 1")
	}
}

func TestValuesInitWithEmptyValues(t *testing.T) {
	_, err := functions.NewValuesFunction([]int{}, 0, 0)
	if err == nil {
		t.Errorf("Expected ValueError for empty values")
	}
}

func TestValuesInitWithIncorrectOptionalValue(t *testing.T) {
	_, err := functions.NewValuesFunction([]int{0, 1, 2}, 3, 0)
	if err == nil {
		t.Errorf("Expected ValueError for optional_value not in values")
	}
}

func TestValuesInitWithIncorrectFirstValue(t *testing.T) {
	_, err := functions.NewValuesFunction([]int{0, 1, 2}, 0, 3)
	if err == nil {
		t.Errorf("Expected ValueError for first_value not in values")
	}
}

func TestValuesBump(t *testing.T) {
	funcObj, err := functions.NewValuesFunction([]int{0, 5, 10}, 0, 0)
	if err != nil {
		t.Fatalf("Init error: %v", err)
	}
	if bumped, err := funcObj.BumpVal(0); err != nil || bumped != 5 {
		t.Errorf("Expected bump(0) = 5, got %v with err %v", bumped, err)
	}
}

func TestValuesBumpError(t *testing.T) {
	funcObj, err := functions.NewValuesFunction([]int{0, 5, 10}, 0, 0)
	if err != nil {
		t.Fatalf("Init error: %v", err)
	}
	_, err = funcObj.BumpVal(10)
	if err == nil {
		t.Errorf("Expected error for bumping last value")
	}
}