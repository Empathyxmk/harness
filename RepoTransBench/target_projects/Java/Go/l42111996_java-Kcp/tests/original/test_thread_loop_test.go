package original

import (
	"sync"
	"testing"
	"time"
)

func threadLoop(work func(), count int, wg *sync.WaitGroup) {
	for i := 0; i < count; i++ {
		go func() {
			defer wg.Done()
			work()
		}()
	}
}

func TestThreadLoopExecution(t *testing.T) {
	const numThreads = 25
	const incrementsPerThread = 100

	var sum int64
	var mu sync.Mutex

	increment := func() {
		for i := 0; i < incrementsPerThread; i++ {
			mu.Lock()
			sum++
			mu.Unlock()
			time.Sleep(2 * time.Millisecond) // Simulate work/yielding
		}
	}

	var wg sync.WaitGroup
	wg.Add(numThreads)
	threadLoop(increment, numThreads, &wg)
	wg.Wait()

	want := int64(numThreads * incrementsPerThread)
	if sum != want {
		t.Errorf("Expected counter value %d, got %d", want, sum)
	}
}

func TestThreadLoopYielding(t *testing.T) {
	const numThreads = 10
	const value = 42

	var results []int
	var mu sync.Mutex

	work := func(i int) func() {
		return func() {
			// simulate waiting and writing result
			time.Sleep(time.Duration(i) * 5 * time.Millisecond)
			mu.Lock()
			results = append(results, value+i)
			mu.Unlock()
		}
	}

	var wg sync.WaitGroup
	wg.Add(numThreads)
	for i := 0; i < numThreads; i++ {
		go func(idx int) {
			defer wg.Done()
			work(idx)()
		}(i)
	}
	wg.Wait()

	// Ensure all results were recorded and values are correct and unique
	if len(results) != numThreads {
		t.Errorf("Expected %d results, got %d", numThreads, len(results))
	}

	valueMap := make(map[int]bool)
	for _, v := range results {
		if valueMap[v] {
			t.Errorf("Duplicate result: %d", v)
		}
		valueMap[v] = true
		if v < value || v > value+numThreads-1 {
			t.Errorf("Unexpected result value: %d", v)
		}
	}
}