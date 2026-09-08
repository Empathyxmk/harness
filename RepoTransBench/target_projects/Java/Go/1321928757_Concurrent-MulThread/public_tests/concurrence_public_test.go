package public_tests

import (
	"sync"
	"sync/atomic"
	"testing"
)

func TestLowerConcurrency(t *testing.T) {
	var atomicInteger int32
	const nThreads = 5
	const nTasks = 20
	const increments = 10

	var wgStart sync.WaitGroup
	var wgDone sync.WaitGroup

	wgStart.Add(nTasks)
	wgDone.Add(nTasks)

	workerPool := make(chan struct{}, nThreads)

	for i := 0; i < nTasks; i++ {
		go func() {
			wgStart.Done()
			wgStart.Wait()

			workerPool <- struct{}{}
			for j := 0; j < increments; j++ {
				atomic.AddInt32(&atomicInteger, 1)
			}
			<-workerPool

			wgDone.Done()
		}()
	}

	wgStart.Wait()
	wgDone.Wait()

	expected := int32(nTasks * increments)
	if atomicInteger != expected {
		t.Errorf("expected atomicInteger == %d, got %d", expected, atomicInteger)
	}
}