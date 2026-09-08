package original

import (
	"testing"
	"time"
)

func TestTimerBasicAndElapsed(t *testing.T) {
	start := time.Now()
	time.Sleep(10 * time.Millisecond)
	elapsed1 := time.Since(start)
	if elapsed1 <= 0 {
		t.Fatal("timer elapsed should be > 0")
	}
	time.Sleep(10 * time.Millisecond)
	elapsed2 := time.Since(start)
	if elapsed2 <= elapsed1 {
		t.Fatalf("timer did not advance")
	}
}

func TestTimerStrAndRepr(t *testing.T) {
	t1 := time.Now()
	if t1.IsZero() {
		t.Fatal("timer should not be zero")
	}
	_ = t1.String()
}