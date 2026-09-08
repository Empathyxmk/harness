package public_tests

import "testing"

func TestPerformanceWithDifferentParams(t *testing.T) {
	iterations := 2500
	perIteration := 251
	result := iterations * perIteration
	expected := 627500
	if result != expected {
		t.Errorf("expected %d, got %d", expected, result)
	}
}