package public_tests

import (
	"testing"
	"example.com/calculator"
)

func TestAdd(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Add(4, 7)
	want := 11
	if got != want {
		t.Errorf("Add(4, 7) = %d; want %d", got, want)
	}
}

func TestSubtract(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Subtract(10, 4)
	want := 6
	if got != want {
		t.Errorf("Subtract(10, 4) = %d; want %d", got, want)
	}
}

func TestMultiply(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Multiply(5, 4)
	want := 20
	if got != want {
		t.Errorf("Multiply(5, 4) = %d; want %d", got, want)
	}
}

func TestDivide(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Divide(20, 4)
	want := 5
	if got != want {
		t.Errorf("Divide(20, 4) = %d; want %d", got, want)
	}
}

func TestDivideByZero(t *testing.T) {
	calc := calculator.Calculator{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Divide(17, 0) did not panic; expected IllegalArgumentException")
		} else {
			if _, ok := r.(calculator.IllegalArgumentException); !ok {
				t.Errorf("Divide(17, 0) panicked with wrong type: %T", r)
			}
		}
	}()
	_ = calc.Divide(17, 0)
}