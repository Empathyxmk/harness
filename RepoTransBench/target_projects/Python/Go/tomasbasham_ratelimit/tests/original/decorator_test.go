package original

import (
	"testing"
	"sync"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

// A fake clock struct for deterministic time advancement
type FakeClock struct {
	mu      sync.Mutex
	counter float64
}

func (c *FakeClock) Now() float64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.counter
}
func (c *FakeClock) Increment(sec float64) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.counter += sec
}

type testStruct struct {
	count int
	clock *FakeClock
}

func (ts *testStruct) Increment() {
	ts.count++
}

func (ts *testStruct) IncrementNoException() {
	ts.count++
}

func setupTestStruct() *testStruct {
	clock := &FakeClock{counter: 0}
	ts := &testStruct{count: 0, clock: clock}
	return ts
}

func TestIncrement(t *testing.T) {
	ts := setupTestStruct()
	rl := ratelimit.NewRateLimitDecorator(1, 10, ts.clock.Now, true)
	fn := rl.Decorate(ts.Increment).(func())
	fn()
	if ts.count != 1 {
		t.Errorf("Expected count==1 after 1 increment, got %d", ts.count)
	}
}

func TestException(t *testing.T) {
	ts := setupTestStruct()
	rl := ratelimit.NewRateLimitDecorator(1, 10, ts.clock.Now, true)
	fn := rl.Decorate(ts.Increment).(func())
	fn()
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected RateLimitException panic")
		}
	}()
	fn()
}

func TestReset(t *testing.T) {
	ts := setupTestStruct()
	rl := ratelimit.NewRateLimitDecorator(1, 10, ts.clock.Now, true)
	fn := rl.Decorate(ts.Increment).(func())
	fn()
	ts.clock.Increment(10)
	fn()
	if ts.count != 2 {
		t.Errorf("Expected count==2 after reset, got %d", ts.count)
	}
}

func TestNoException(t *testing.T) {
	ts := setupTestStruct()
	rl := ratelimit.NewRateLimitDecorator(1, 10, ts.clock.Now, false)
	fn := rl.Decorate(ts.IncrementNoException).(func())
	fn()
	fn()
	if ts.count != 1 {
		t.Errorf("Call after limit should be blocked (no increment), got %d", ts.count)
	}
}