package original

import (
	"sync"
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

type dummyClock struct {
	mu    sync.Mutex
	value float64
}

func newDummyClock() *dummyClock {
	return &dummyClock{value: 1000}
}
func (c *dummyClock) Next() float64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	v := c.value
	c.value += 1
	return v
}

func TestDecoratorAllowsCallsWithinLimit(t *testing.T) {
	calls := []int{}
	c := newDummyClock()
	rl := ratelimit.NewRateLimitDecorator(2, 10, c.Next, true)
	fn := rl.Decorate(func(x int) int {
		calls = append(calls, x)
		return x
	}).(func(int) int)
	if fn(2) != 2 {
		t.Fatalf("expected 2")
	}
	if fn(3) != 3 {
		t.Fatalf("expected 3")
	}
	if len(calls) != 2 || calls[0] != 2 || calls[1] != 3 {
		t.Errorf("calls = %v, expected [2,3]", calls)
	}
}

func TestDecoratorRaisesOnExceedingLimit(t *testing.T) {
	c := newDummyClock()
	decoratedCalls := []int{}
	rl := ratelimit.NewRateLimitDecorator(1, 10, c.Next, true)
	fn := rl.Decorate(func(x int) int {
		decoratedCalls = append(decoratedCalls, x)
		return x
	}).(func(int) int)
	fn(1)
	didPanic := false
	func() {
		defer func() {
			if r := recover(); r != nil {
				e, ok := r.(*ratelimit.RateLimitException)
				if ok {
					if e.PeriodRemaining != 9 {
						t.Errorf("PeriodRemaining: expected 9, got %v", e.PeriodRemaining)
					}
					didPanic = true
				}
			}
		}()
		fn(2)
	}()
	if !didPanic {
		t.Errorf("Expected panic")
	}
}

func TestDecoratorReturnsNoneWhenRaiseOnLimitFalse(t *testing.T) {
	c := newDummyClock()
	calls := []int{}
	rl := ratelimit.NewRateLimitDecorator(1, 10, c.Next, false)
	fn := rl.Decorate(func(x int) int {
		calls = append(calls, x)
		return x
	}).(func(int) int)
	val := fn(5)
	if val != 5 {
		t.Errorf("Expected fn(5)=5 got %v", val)
	}
	val2 := fn(6)
	if val2 != 0 {
		t.Errorf("Expected fn(6)=0 (blocked), got %d", val2)
	}
	if len(calls) != 1 || calls[0] != 5 {
		t.Errorf("calls = %v, expected [5]", calls)
	}
}

func TestDecoratorResetsAfterPeriod(t *testing.T) {
	state := struct{ t float64 }{0}
	fakeClock := func() float64 {
		t := state.t
		state.t += 0.1
		return t
	}
	rl := ratelimit.NewRateLimitDecorator(1, 0.05, fakeClock, true)
	fn := rl.Decorate(func(x int) int { return x }).(func(int) int)
	if fn(1) != 1 {
		t.Errorf("expected 1")
	}
	if fn(2) != 2 {
		t.Errorf("expected 2 (after virtual period reset)")
	}
}

func TestSleepAndRetrySleepsAndRetries(t *testing.T) {
	callCount := 0
	sleepPeriods := []float64{}
	fakeSleep := func(p float64) {
		sleepPeriods = append(sleepPeriods, p)
	}
	// SleepAndRetry replaces time.Sleep in the decorator, so we use this function for testing.

	alwaysFail := func() interface{} {
		if callCount == 0 {
			callCount++
			panic(&ratelimit.RateLimitException{"too many", 0.01})
		}
		return "worked!"
	}
	result := ratelimit.SleepAndRetry(alwaysFail, fakeSleep)
	if result != "worked!" {
		t.Errorf("Expected 'worked!', got %v", result)
	}
	if len(sleepPeriods) != 1 || sleepPeriods[0] != 0.01 {
		t.Errorf("Expected sleepPeriods=[0.01], got %v", sleepPeriods)
	}
}

func TestPeriodRemainingReturnsProperValue(t *testing.T) {
	state := struct {
		t     float64
		reset float64
	}{500, 498}
	fakeClock := func() float64 { return state.t }
	rl := ratelimit.NewRateLimitDecorator(1, 10, fakeClock, true)
	rl.SetLastReset(498)
	state.t = 505
	remaining := rl.PeriodRemaining()
	if remaining != 3 {
		t.Errorf("Expected period remaining=3, got %v", remaining)
	}
}