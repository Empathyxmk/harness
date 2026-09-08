package original

import (
	"math"
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestNowReturnsCallableAndReturnsFloat(t *testing.T) {
	fn := ratelimit.Now()
	if fn == nil {
		t.Fatalf("Expected callable, got nil")
	}
	val := fn()
	if _, ok := interface{}(val).(float64); !ok {
		t.Errorf("Expected float64 value but got %T", val)
	}
}

func TestNowFallback(t *testing.T) {
	origMonotonic := ratelimit.FakeDisableMonotonic()
	defer origMonotonic()
	fn := ratelimit.Now()
	if fn == nil {
		t.Fatalf("Expected callable, got nil")
	}
	n := fn()
	ctime := float64(time.Now().UnixNano()) / 1e9
	if math.Abs(n-ctime) > 1 {
		t.Errorf("now fallback function too far from system time: got %v, want approx %v", n, ctime)
	}
}