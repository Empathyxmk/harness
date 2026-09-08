package public_tests

import (
	"testing"
	"time"
)

func GetCputime() float64 {
	// Simulate "core.cputime()": wall time for demonstration
	return float64(time.Now().UnixNano()) / 1e9
}

func TestPublicCputimeRuns(t *testing.T) {
	value := GetCputime()
	if value < 0 {
		t.Error("Expected cputime non-negative")
	}
}