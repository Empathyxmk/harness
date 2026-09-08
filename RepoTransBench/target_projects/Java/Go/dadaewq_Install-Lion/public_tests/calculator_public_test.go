package public_tests

import (
	"testing"

	"dadaewq_install_lion"
)

func TestAdd(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Add(4, 7); got != 11 {
		t.Errorf("Add(4, 7) = %d; want 11", got)
	}
	if got := calculator.Add(6, -3); got != 3 {
		t.Errorf("Add(6, -3) = %d; want 3", got)
	}
}

func TestSubtract(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Subtract(10, 2); got != 8 {
		t.Errorf("Subtract(10, 2) = %d; want 8", got)
	}
	if got := calculator.Subtract(9, -3); got != 12 {
		t.Errorf("Subtract(9, -3) = %d; want 12", got)
	}
}

func TestMultiply(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Multiply(5, 7); got != 35 {
		t.Errorf("Multiply(5, 7) = %d; want 35", got)
	}
	if got := calculator.Multiply(4, -5); got != -20 {
		t.Errorf("Multiply(4, -5) = %d; want -20", got)
	}
}

func TestDivide(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Divide(72, 8); got != 9 {
		t.Errorf("Divide(72, 8) = %d; want 9", got)
	}
	if got := calculator.Divide(12, -3); got != -4 {
		t.Errorf("Divide(12, -3) = %d; want -4", got)
	}
}

func TestDivideByZero(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Divide by zero did not panic")
		} else {
			if r != "Divider cannot be zero." {
				t.Errorf("Unexpected panic message: got %v, want %v", r, "Divider cannot be zero.")
			}
		}
	}()
	calculator := dadaewq_install_lion.NewCalculator()
	_ = calculator.Divide(8, 0)
}