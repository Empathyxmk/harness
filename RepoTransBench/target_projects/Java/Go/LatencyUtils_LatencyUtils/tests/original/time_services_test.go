package tests

import (
	"testing"
)

func TestNanoTimeAndMillisStatic(t *testing.T) {
	n1 := NanoTime()
	m1 := CurrentTimeMillis()
	if n1 <= 0 {
		t.Errorf("NanoTime returned %d, expected > 0", n1)
	}
	if m1 <= 0 {
		t.Errorf("CurrentTimeMillis returned %d, expected > 0", m1)
	}
}