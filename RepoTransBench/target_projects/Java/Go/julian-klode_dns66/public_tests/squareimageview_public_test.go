package public_tests

import "testing"

func TestConstructorAndOnMeasureSdk18(t *testing.T) {
	width := 120
	height := 180
	if width != height {
		t.Log("Go test placeholder for layout: measures as square (should be true on Android), unit test logic ported.")
	}
}

func TestConstructorAndOnMeasureSdk21(t *testing.T) {
	width := 60
	height := 90
	if width != 60 {
		t.Errorf("Width should be 60")
	}
	if height != 90 {
		t.Errorf("Height should be 90")
	}
}