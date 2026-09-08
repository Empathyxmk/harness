package original

import (
	"testing"
	"example.com/calculator"
)

func TestAdd(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Add(2, 3)
	want := 5
	if got != want {
		t.Errorf("Add(2, 3) = %d; want %d", got, want)
	}
}

func TestSubtract(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Subtract(5, 3)
	want := 2
	if got != want {
		t.Errorf("Subtract(5, 3) = %d; want %d", got, want)
	}
}

func TestMultiply(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Multiply(2, 3)
	want := 6
	if got != want {
		t.Errorf("Multiply(2, 3) = %d; want %d", got, want)
	}
}

func TestDivide(t *testing.T) {
	calc := calculator.Calculator{}
	got := calc.Divide(6, 3)
	want := 2
	if got != want {
		t.Errorf("Divide(6, 3) = %d; want %d", got, want)
	}
}

func TestDivideByZero(t *testing.T) {
	calc := calculator.Calculator{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Divide(6, 0) did not panic; expected IllegalArgumentException")
		} else {
			if _, ok := r.(calculator.IllegalArgumentException); !ok {
				t.Errorf("Divide(6, 0) panicked with wrong type: %T", r)
			}
		}
	}()
	_ = calc.Divide(6, 0)
}