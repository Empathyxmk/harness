package original

import (
	"math"
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestConstructorClampsCalls(t *testing.T) {
	type testCase struct {
		calls   float64
		expect  int
	}
	testCases := []testCase{
		{-5, 1},
		{math.Exp2(100), int(^uint(0) >> 1)}, // sys.maxsize
		{3.9, 3},
	}
	for _, tc := range testCases {
		rld := ratelimit.NewRateLimitDecorator(tc.calls, 1, nil, true)
		if rld.ClampedCalls() != tc.expect {
			t.Errorf("calls was %v, expected clamped %d, got %d", tc.calls, tc.expect, rld.ClampedCalls())
		}
	}
}

func TestDecoratorRateLimitRaises(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(1, 0.05, nil, true)
	count := 0
	f := rl.Decorate(func() string {
		count++
		return "foo"
	}).(func() string)
	if f() != "foo" {
		t.Errorf("Expected foo")
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic (RateLimitException)")
		}
	}()
	f() // should panic
	time.Sleep(60 * time.Millisecond)
	if f() != "foo" {
		t.Errorf("After reset, expected foo")
	}
}

func TestDecoratorDoesNotRaise(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(1, 0.05, nil, false)
	result := 0
	f := rl.Decorate(func() int {
		result += 1
		return result
	}).(func() int)
	if f() != 1 {
		t.Errorf("Expected first result 1")
	}
	time.Sleep(60 * time.Millisecond)
	if f() != 2 {
		t.Errorf("Expected second result 2 after period reset")
	}
}

func TestThreadSafety(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(10, 1, nil, true)
	dummy := func() int {
		return 42
	}
	wrapped := rl.Decorate(dummy).(func() int)
	_ = wrapped()
	_ = wrapped()
	// After at least two calls, lock should exist. Use reflection or exposed test method if needed.
	if !rl.HasLock() {
		t.Errorf("Expected lock to be present in RateLimitDecorator after two calls")
	}
}