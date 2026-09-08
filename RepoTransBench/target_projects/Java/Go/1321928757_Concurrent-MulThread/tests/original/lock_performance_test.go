package original

import (
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestLockPerformance(t *testing.T) {
	const READ_THREADS = 10
	const WRITE_THREADS = 2
	const ITERATIONS = 100000

	var sharedResource int64

	var readLock = &sync.RWMutex{}
	var wg sync.WaitGroup

	// Start readers
	for i := 0; i < READ_THREADS; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < ITERATIONS; j++ {
				readLock.RLock()
				_ = atomic.LoadInt64(&sharedResource)
				readLock.RUnlock()
			}
		}()
	}

	// Start writers
	for i := 0; i < WRITE_THREADS; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < ITERATIONS; j++ {
				readLock.Lock()
				sharedResource++
				readLock.Unlock()
			}
		}()
	}

	start := time.Now()
	wg.Wait()
	durRW := time.Since(start)
	t.Logf("ReentrantReadWriteLock (Go: sync.RWMutex) time: %v", durRW)
}