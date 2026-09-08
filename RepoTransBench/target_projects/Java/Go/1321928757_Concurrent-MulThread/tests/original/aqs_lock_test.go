package original

import (
	"sync"
	"testing"
	"time"
)

// OnlySyncByAQS mimics a basic exclusive lock using sync.Mutex for demonstration.
type OnlySyncByAQS struct {
	mu sync.Mutex
}

// Lock acquires the lock.
func (a *OnlySyncByAQS) Lock() {
	a.mu.Lock()
}

// Unlock releases the lock.
func (a *OnlySyncByAQS) Unlock() {
	a.mu.Unlock()
}

// Test class simulation.
type aqsTestHelper struct {
	lock *OnlySyncByAQS
}

func newAqsTestHelper() *aqsTestHelper {
	return &aqsTestHelper{lock: &OnlySyncByAQS{}}
}

func (t *aqsTestHelper) Use() {
	t.lock.Lock()
	defer t.lock.Unlock()
	time.Sleep(1 * time.Second)
}

func TestAQSMultiGoroutine(t *testing.T) {
	helper := newAqsTestHelper()
	var wg sync.WaitGroup
	numGoroutines := 3
	wg.Add(numGoroutines)
	for i := 0; i < numGoroutines; i++ {
		go func() {
			defer wg.Done()
			helper.Use()
		}()
	}
	wg.Wait()
}