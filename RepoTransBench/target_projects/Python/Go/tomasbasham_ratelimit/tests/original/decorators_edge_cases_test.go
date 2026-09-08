package original

import (
	"reflect"
	"runtime"
	"sort"
	"sync"
	"testing"
	"time"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestClampedCallsMinAndMax(t *testing.T) {
	d := ratelimit.NewRateLimitDecorator(-9, 1, func() float64 { return 0 }, true)
	if d.ClampedCalls() != 1 {
		t.Errorf("ClampedCalls < 1 not set to 1, got %d", d.ClampedCalls())
	}
	d2 := ratelimit.NewRateLimitDecorator(float64(int64(^uint(0)>>1))+123456, 1, func() float64 { return 0 }, true)
	if d2.ClampedCalls() != int(^uint(0)>>1) {
		t.Errorf("ClampedCalls > max set to maxsize, got %d", d2.ClampedCalls())
	}
}

func TestDecoratorThreadSafety(t *testing.T) {
	result := []int{}
	dec := ratelimit.NewRateLimitDecorator(2, 1, func() float64 { return 0 }, true)
	fn := dec.Decorate(func(x int) int {
		result = append(result, x)
		return x
	}).(func(int) int)
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		defer wg.Done()
		fn(1)
	}()
	go func() {
		defer wg.Done()
		fn(2)
	}()
	wg.Wait()
	sort.Ints(result)
	if !reflect.DeepEqual(result, []int{1, 2}) {
		t.Errorf("expected [1,2], got %+v", result)
	}
}

func TestPeriodRemainingZero(t *testing.T) {
	fakeClock := func() float64 { return 20 }
	dec := ratelimit.NewRateLimitDecorator(2, 5, fakeClock, true)
	dec.SetLastReset(15)
	called := []string{}
	fn := dec.Decorate(func() int {
		called = append(called, "called")
		return 123
	}).(func() int)
	if fn() != 123 {
		t.Errorf("Expected fn()==123")
	}
	if fn() != 123 {
		t.Errorf("Second call should still work")
	}
}

func TestPeriodRemainingNegative(t *testing.T) {
	state := struct{ t float64 }{0}
	fakeClock := func() float64 {
		val := state.t
		state.t += 100
		return val
	}
	dec := ratelimit.NewRateLimitDecorator(1, 1, fakeClock, true)
	called := []int{}
	fn := dec.Decorate(func() { called = append(called, 1) }).(func())
	fn()
	fn()
	if len(called) != 2 {
		t.Errorf("Expected called twice, got %d", len(called))
	}
}