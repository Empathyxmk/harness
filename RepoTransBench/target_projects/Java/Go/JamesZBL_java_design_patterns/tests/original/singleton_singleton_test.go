package original

import (
	"sync"
	"testing"
)

// singletonTestSuite provides the core singleton pattern test logic
func singletonTestSuite(t *testing.T, instanceFunc func() interface{}) {
	// Single thread
	a := instanceFunc()
	b := instanceFunc()
	c := instanceFunc()
	if a != b || b != c {
		t.Errorf("singleton instance not same in same thread")
	}

	// Multi-goroutine
	const N = 5000
	var wg sync.WaitGroup
	results := make([]interface{}, N)
	for i := 0; i < N; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			results[i] = instanceFunc()
		}(i)
	}
	wg.Wait()
	expected := instanceFunc()
	for i, res := range results {
		if res == nil {
			t.Errorf("instance %d is nil", i)
		}
		if res != expected {
			t.Errorf("instance %d is not singleton", i)
		}
	}
}