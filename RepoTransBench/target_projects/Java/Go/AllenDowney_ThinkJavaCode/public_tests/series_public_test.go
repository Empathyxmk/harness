package public_tests

import (
	"testing"
)

// geometricSeriesSum computes a*(r^0 + r^1 + ... + r^(n-1))
func geometricSeriesSum(a, r, n int) int {
	total := 0
	for i := 0; i < n; i++ {
		total += a * pow(r, i)
	}
	return total
}
func arithmeticSeriesSum(a, d, n int) int {
	total := 0
	num := a
	for i := 0; i < n; i++ {
		total += num
		num += d
	}
	return total
}
func pow(base, exp int) int {
	result := 1
	for i := 0; i < exp; i++ {
		result *= base
	}
	return result
}

func TestGeometricSeriesDifferentData(t *testing.T) {
	// a=3, r=2, n=4 → 3 * (1+2+4+8)=3*15=45
	result := geometricSeriesSum(3, 2, 4)
	if result != 45 {
		t.Errorf("Expected 45, got %d", result)
	}
	if geometricSeriesSum(1, 10, 3) != 111 {
		t.Errorf("Expected 111, got %d", geometricSeriesSum(1, 10, 3))
	}
}

func TestArithmeticSeriesDifferentData(t *testing.T) {
	// a=2, d=5, n=4 → 2+7+12+17=38
	result := arithmeticSeriesSum(2, 5, 4)
	if result != 38 {
		t.Errorf("Expected 38, got %d", result)
	}
	if arithmeticSeriesSum(3, 0, 5) != 15 {
		t.Errorf("Expected 15, got %d", arithmeticSeriesSum(3, 0, 5))
	}
}