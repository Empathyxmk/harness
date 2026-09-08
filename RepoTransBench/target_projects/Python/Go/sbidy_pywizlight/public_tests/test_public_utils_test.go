package public_tests

import "testing"

func clamp(val, min, max int) int {
	if val < min {
		return min
	}
	if val > max {
		return max
	}
	return val
}

func TestClampPublic(t *testing.T) {
	if clamp(135, 100, 140) != 135 {
		t.Errorf("clamp(135,100,140) expected 135")
	}
	if clamp(90, 100, 140) != 100 {
		t.Errorf("clamp(90,100,140) expected 100")
	}
	if clamp(145, 100, 140) != 140 {
		t.Errorf("clamp(145,100,140) expected 140")
	}
}