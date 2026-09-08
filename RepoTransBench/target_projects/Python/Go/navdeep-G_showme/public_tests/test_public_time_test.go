package public_tests

import (
	"testing"
	"time"
)

func GetTime() float64 {
	// Simulate "core.time()"
	return float64(time.Now().UnixNano()) / 1e9
}

func TestTimeTypeAndRange(t *testing.T) {
	value := GetTime()
	if value < 0 {
		t.Errorf("Expected non-negative time, got %v", value)
	}
	if value > 100000 {
		t.Errorf("Time value unexpectedly high: %v", value)
	}
}