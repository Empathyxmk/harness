package public_tests

import "testing"

func celsiusToFahrenheit(c float64) float64 {
	return c*9/5 + 32
}
func fahrenheitToCelsius(f float64) float64 {
	return (f - 32) * 5 / 9
}

func TestCelsiusToFahrenheitPublicData(t *testing.T) {
	tc := []struct {
		c, expected float64
	}{
		{0, 32.0}, {50, 122.0}, {20, 68.0}, {37, 98.6},
	}
	for _, x := range tc {
		got := celsiusToFahrenheit(x.c)
		if abs(got-x.expected) > 0.01 {
			t.Errorf("celsiusToFahrenheit(%v): got %v, want %v", x.c, got, x.expected)
		}
	}
}

func TestFahrenheitToCelsiusPublicData(t *testing.T) {
	tc := []struct {
		f, expected float64
	}{
		{32, 0.0}, {212, 100.0}, {104, 40.0}, {41, 5.0},
	}
	for _, x := range tc {
		got := fahrenheitToCelsius(x.f)
		if abs(got-x.expected) > 0.01 {
			t.Errorf("fahrenheitToCelsius(%v): got %v, want %v", x.f, got, x.expected)
		}
	}
}

func abs(x float64) float64 {
	if x < 0 {
		return -x
	}
	return x
}