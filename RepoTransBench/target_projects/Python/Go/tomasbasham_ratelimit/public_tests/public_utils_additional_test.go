package public_tests

import (
	"math"
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicNowMonotonicity(t *testing.T) {
	t1 := ratelimit.Now()()
	time.Sleep(10 * time.Millisecond)
	t2 := ratelimit.Now()()
	if t2 < t1 {
		t.Errorf("Expected t2 >= t1, got t1=%v, t2=%v", t1, t2)
	}
}

func TestPublicNowCloseToTimeTime(t *testing.T) {
	t1 := ratelimit.Now()()
	t2 := float64(time.Now().UnixNano()) / 1e9
	if math.Abs(t2-t1) > 1 {
		t.Errorf("now() too far from time.Now: got t1=%v, t2=%v", t1, t2)
	}
}