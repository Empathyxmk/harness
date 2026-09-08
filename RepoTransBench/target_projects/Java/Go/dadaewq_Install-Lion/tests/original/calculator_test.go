package original

import (
	"testing"

	"dadaewq_install_lion"
)

func TestAdd(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Add(2, 3); got != 5 {
		t.Errorf("Add(2, 3) = %d; want 5", got)
	}
	if got := calculator.Add(2, -3); got != -1 {
		t.Errorf("Add(2, -3) = %d; want -1", got)
	}
}

func TestSubtract(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Subtract(2, 3); got != -1 {
		t.Errorf("Subtract(2, 3) = %d; want -1", got)
	}
	if got := calculator.Subtract(2, -3); got != 5 {
		t.Errorf("Subtract(2, -3) = %d; want 5", got)
	}
}

func TestMultiply(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Multiply(2, 3); got != 6 {
		t.Errorf("Multiply(2, 3) = %d; want 6", got)
	}
	if got := calculator.Multiply(2, -3); got != -6 {
		t.Errorf("Multiply(2, -3) = %d; want -6", got)
	}
}

func TestDivide(t *testing.T) {
	calculator := dadaewq_install_lion.NewCalculator()
	if got := calculator.Divide(6, 3); got != 2 {
		t.Errorf("Divide(6, 3) = %d; want 2", got)
	}
	if got := calculator.Divide(6, -3); got != -2 {
		t.Errorf("Divide(6, -3) = %d; want -2", got)
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
	_ = calculator.Divide(1, 0)
}