package public_tests

import (
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicNowTypeAndIncreasing(t *testing.T) {
	t1 := ratelimit.Now()()
	time.Sleep(5 * time.Millisecond)
	t2 := ratelimit.Now()()
	if t2 < t1 {
		t.Errorf("t2 < t1, got t1=%v t2=%v", t1, t2)
	}
}

func TestPublicNowMonotonic(t *testing.T) {
	vals := []float64{ratelimit.Now()(), ratelimit.Now()(), ratelimit.Now()()}
	if vals[1] < vals[0] {
		t.Errorf("vals[1] < vals[0]: %v < %v", vals[1], vals[0])
	}
	if vals[2] < vals[1] {
		t.Errorf("vals[2] < vals[1]: %v < %v", vals[2], vals[1])
	}
}