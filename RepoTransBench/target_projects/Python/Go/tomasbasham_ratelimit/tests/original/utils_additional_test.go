package original

import (
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestNowReturnsMonotonicOrTime(t *testing.T) {
	fn := ratelimit.Now()
	t1 := fn()
	time.Sleep(10 * time.Millisecond)
	t2 := fn()
	if t2 <= t1 {
		t.Errorf("Expected t2 > t1, got t1=%v, t2=%v", t1, t2)
	}

	// Simulate removing monotonic
	origMonotonic := ratelimit.FakeDisableMonotonic()
	defer origMonotonic()
	fn = ratelimit.Now()
	t3 := fn()
	time.Sleep(10 * time.Millisecond)
	t4 := fn()
	if t4 <= t3 {
		t.Errorf("Expected t4 > t3, got t3=%v, t4=%v", t3, t4)
	}
}