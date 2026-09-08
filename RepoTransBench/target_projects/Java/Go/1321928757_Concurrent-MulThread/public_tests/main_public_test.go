package public_tests

import (
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

type TestThreadPool struct {
	wg sync.WaitGroup
}

func (p *TestThreadPool) execute(fn func()) {
	p.wg.Add(1)
	go func() {
		defer p.wg.Done()
		fn()
	}()
}

func (p *TestThreadPool) shutdown() {
	p.wg.Wait()
}

// Public thread pool test: sum a sequence of numbers using custom thread pool like the Java code.
func TestPublicThreadPool(t *testing.T) {
	var sum int32
	pool := TestThreadPool{}
	numberOfTasks := 7

	for i := 0; i < numberOfTasks; i++ {
		idx := i
		pool.execute(func() {
			atomic.AddInt32(&sum, int32(idx))
		})
	}

	pool.shutdown()

	expected := int32(0)
	for i := 0; i < numberOfTasks; i++ {
		expected += int32(i)
	}
	if sum != expected {
		t.Errorf("expected sum == %d, got %d", expected, sum)
	}
}