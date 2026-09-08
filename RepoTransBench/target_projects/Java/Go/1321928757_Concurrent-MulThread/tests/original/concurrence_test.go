package original

import (
	"log"
	"sync"
	"sync/atomic"
	"testing"
)

func TestConcurrenceSimulatedHighLoad(t *testing.T) {
	var atomicInteger int32
	const numWorkers = 10
	const numTasks = 1000
	const incrementsPerTask = 1000

	var wgStart sync.WaitGroup   // to simulate "all ready at once"
	var wgDone sync.WaitGroup    // to wait all finish

	wgStart.Add(numTasks)
	wgDone.Add(numTasks)

	workerPool := make(chan struct{}, numWorkers)

	for i := 0; i < numTasks; i++ {
		go func() {
			wgStart.Done() // signal "ready"
			wgStart.Wait() // wait until all others are ready

			workerPool <- struct{}{} // block if no worker slot
			for j := 0; j < incrementsPerTask; j++ {
				atomic.AddInt32(&atomicInteger, 1)
			}
			<-workerPool
			wgDone.Done() // signal finished
		}()
	}

	wgStart.Wait() // all ready, start all
	wgDone.Wait()  // all finished

	if atomicInteger != int32(numTasks*incrementsPerTask) {
		t.Errorf("Expected atomicInteger == %d, got %d", numTasks*incrementsPerTask, atomicInteger)
	}
	log.Printf("atomicInteger的值为: %d", atomicInteger)
}