package public_tests

import (
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicSimpleLimit(t *testing.T) {
	d := ratelimit.NewRateLimitDecorator(3, 0.04, nil, true)
	calls := []int{}
	myfun := d.Decorate(func() int {
		calls = append(calls, 2)
		sum := 0
		for _, v := range calls {
			sum += v
		}
		return sum
	}).(func() int)
	if myfun() != 2 {
		t.Errorf("Expected sum 2 at 1st call")
	}
	if myfun() != 4 {
		t.Errorf("Expected sum 4")
	}
	if myfun() != 6 {
		t.Errorf("Expected sum 6")
	}
	didPanic := false
	func() {
		defer func() {
			if r := recover(); r != nil {
				didPanic = true
			}
		}()
		myfun()
	}()
	if !didPanic {
		t.Errorf("Expected panic on 4th call due to RateLimitException")
	}
	time.Sleep(45 * time.Millisecond)
	if myfun() != 8 {
		t.Errorf("Expected sum 8 after waiting for rate reset")
	}
}

func TestPublicSleepAndRetry(t *testing.T) {
	d := ratelimit.NewRateLimitDecorator(1, 0.02, nil, true)
	fn := ratelimit.SleepAndRetry(d.Decorate(func() int { return 24 }).(func() int), nil).(func() int)
	if fn() != 24 {
		t.Errorf("Expected 24")
	}
	t0 := time.Now()
	if fn() != 24 {
		t.Errorf("Expected 24 again")
	}
	elapsed := time.Since(t0)
	if elapsed < 20*time.Millisecond {
		t.Errorf("Expected at least 20ms elapsed: got %v", elapsed)
	}
}

func TestPublicRaiseOnLimitFalse(t *testing.T) {
	d := ratelimit.NewRateLimitDecorator(1, 0.03, nil, false)
	track := []int{}
	fun := d.Decorate(func() int {
		track = append(track, len(track)+1)
		return track[len(track)-1]
	}).(func() int)
	if fun() != 1 {
		t.Errorf("Expected 1st call=1")
	}
	if fun() != 0 {
		t.Errorf("Expected 2nd call blocked returns 0")
	}
	time.Sleep(35 * time.Millisecond)
	if fun() != 2 {
		t.Errorf("Expected call=2 after period")
	}
}