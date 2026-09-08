package public_tests

import (
	"strings"
	"testing"
)

func Upper(s string) string      { return strings.ToUpper(s) }
func Add(a, b int) int          { return a + b }
func Subtract(a, b int) int     { return a - b }
func Multiply(a, b int) int     { return a * b }
func Divide(a, b int) float64   { return float64(a) / float64(b) }

func TestAdditionalFunctionality(t *testing.T) {
	if Upper("testing") != "TESTING" {
		t.Error("Upper failed")
	}
	if Add(101, 21) != 122 {
		t.Error("Add failed")
	}
	if Subtract(45, 14) != 31 {
		t.Error("Subtract failed")
	}
	if Multiply(13, 4) != 52 {
		t.Error("Multiply failed")
	}
	if Divide(80, 4) != 20.0 {
		t.Error("Divide failed")
	}
	if Divide(77, 5) != 15.4 {
		t.Error("Divide(77,5) failed")
	}
	if Add(-5, -2) != -7 {
		t.Error("Add(-5,-2) failed")
	}
}