package public_tests

import (
	"sync"
	"testing"
	"time"
)

// OnlySyncByAQS uses sync.Mutex to mimic a custom lock for demonstration.
type OnlySyncByAQS struct {
	mu sync.Mutex
}

func (l *OnlySyncByAQS) Lock()   { l.mu.Lock() }
func (l *OnlySyncByAQS) Unlock() { l.mu.Unlock() }

func TestCustomAQSLockMultipleThreads(t *testing.T) {
	lock := &OnlySyncByAQS{}
	numThreads := 4
	count := 0
	var wg sync.WaitGroup
	wg.Add(numThreads)
	for i := 0; i < numThreads; i++ {
		go func() {
			lock.Lock()
			count++
			time.Sleep(250 * time.Millisecond)
			lock.Unlock()
			wg.Done()
		}()
	}
	wg.Wait()
	if count != numThreads {
		t.Errorf("expected count == %d, got %d", numThreads, count)
	}
}