package public_tests

import (
	"math"
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicConstructorClampsCalls(t *testing.T) {
	type testCase struct {
		calls   float64
		expect  int
	}
	testCases := []testCase{
		{0, 1},
		{float64(int64(^uint(0)>>1) + 100), int(^uint(0)>>1)},
		{7.8, 7},
	}
	for _, tc := range testCases {
		rld := ratelimit.NewRateLimitDecorator(tc.calls, 2, nil, true)
		if rld.ClampedCalls() != tc.expect {
			t.Errorf("Input %v: expected clamped_calls %d, got %d", tc.calls, tc.expect, rld.ClampedCalls())
		}
	}
}

func TestPublicDecoratorRateLimitRaises(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(2, 0.03, nil, true)
	cnt := 0
	f := rl.Decorate(func() string {
		cnt++
		return "bar"
	}).(func() string)
	if f() != "bar" {
		t.Errorf("Should return bar")
	}
	if f() != "bar" {
		t.Errorf("Should return bar again (within limit)")
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic on third call")
		}
	}()
	f() // Should panic
	time.Sleep(35 * time.Millisecond)
	if f() != "bar" {
		t.Errorf("Should return bar after rate window reset")
	}
}

func TestPublicDecoratorDoesNotRaise(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(2, 0.04, nil, false)
	result := 0
	bar := rl.Decorate(func() int {
		result++
		return result
	}).(func() int)
	if bar() != 1 {
		t.Errorf("Expected bar()==1")
	}
	if bar() != 2 {
		t.Errorf("Expected bar()==2")
	}
	time.Sleep(45 * time.Millisecond)
	if bar() != 3 {
		t.Errorf("Expected bar()==3 after period")
	}
}

func TestPublicThreadSafety(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(4, 1, nil, true)
	dummy2 := func() int { return 24 }
	wrapped := rl.Decorate(dummy2).(func() int)
	for i := 0; i < 3; i++ {
		wrapped()
	}
	if !rl.HasLock() {
		t.Errorf("Expected lock to exist in RateLimitDecorator after several calls")
	}
}