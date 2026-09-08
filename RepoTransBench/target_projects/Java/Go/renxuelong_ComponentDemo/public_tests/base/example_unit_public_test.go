package base

import (
	"testing"
)

func TestStringConcatIsCorrect(t *testing.T) {
	a := "base"
	b := "Public"
	if a+b != "basePublic" {
		t.Errorf(`Expected "basePublic", got %q`, a+b)
	}
}

func TestIntComparisonIsCorrect(t *testing.T) {
	if !(100 > 99) {
		t.Error("Expected 100 > 99 to be true")
	}
}