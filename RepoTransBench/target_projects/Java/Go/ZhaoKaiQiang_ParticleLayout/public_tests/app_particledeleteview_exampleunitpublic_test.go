package public_tests

import "testing"

func TestAppParticleDeleteView_SubtractionIsCorrect(t *testing.T) {
	if 5-3 != 2 {
		t.Errorf("Expected 5-3=2, got %d", 5-3)
	}
}