package public_tests

import (
	"testing"
)

func TestNanoTimeAndForward(t *testing.T) {
	start := NanoTime()
	MoveTimeForwardMsec(16)
	end := NanoTime()
	if end != start+16_000_000 {
		t.Errorf("expected nano time %d, got %d", start+16_000_000, end)
	}
}