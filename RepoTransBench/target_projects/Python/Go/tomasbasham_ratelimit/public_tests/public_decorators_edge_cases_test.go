package public_tests

import (
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicNegativePeriod(t *testing.T) {
	d := ratelimit.NewRateLimitDecorator(1, -2, nil, true)
	callcount := []int{}
	f := d.Decorate(func() int {
		callcount = append(callcount, 1)
		return 7
	}).(func() int)
	if f() != 7 {
		t.Errorf("Expected 7 on first call")
	}
	didPanic := false
	func() {
		defer func() {
			if r := recover(); r != nil {
				didPanic = true
			}
		}()
		f()
	}()
	if !didPanic {
		t.Errorf("Expected panic after window reset (negative period triggers immediate reset)")
	}
}

func TestPublicSleepAndRetrySucceeds(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(1, 0.02, nil, true)
	callTimes := []time.Time{}
	fun := rl.Decorate(func() int {
		callTimes = append(callTimes, time.Now())
		return 17
	}).(func() int)
	fun = ratelimit.SleepAndRetry(fun, nil).(func() int)
	if fun() != 17 {
		t.Errorf("First call should be 17")
	}
	t0 := time.Now()
	if fun() != 17 {
		t.Errorf("Second call should be 17")
	}
	elapsed := time.Since(t0)
	if elapsed < 20*time.Millisecond {
		t.Errorf("Second call should sleep for period")
	}
}

func TestPublicSleepAndRetryMultiple(t *testing.T) {
	rl := ratelimit.NewRateLimitDecorator(2, 0.015, nil, true)
	counter := 0
	g := rl.Decorate(func() int {
		counter += 2
		return counter
	}).(func() int)
	g = ratelimit.SleepAndRetry(g, nil).(func() int)
	if g() != 2 {
		t.Errorf("1st call: expected 2")
	}
	if g() != 4 {
		t.Errorf("2nd call: expected 4")
	}
	t0 := time.Now()
	val := g()
	if val != 6 {
		t.Errorf("3rd call: expected 6, got %d", val)
	}
	if counter != 6 {
		t.Errorf("Counter should be 6, got %d", counter)
	}
	elapsed := time.Since(t0)
	if elapsed < 15*time.Millisecond {
		t.Errorf("Should be rate-limited and sleep; elapsed=%v", elapsed)
	}
}