package original

import (
	"fmt"
	"sync"
	"testing"
	"time"
)

type DummyPool struct {
	wg sync.WaitGroup
}

func (d *DummyPool) Execute(fn func()) {
	d.wg.Add(1)
	go func() {
		defer d.wg.Done()
		fn()
	}()
}

func (d *DummyPool) Shutdown() {
	d.wg.Wait()
}

func TestManualThreadPool(t *testing.T) {
	var pool DummyPool

	taskCount := 15
	for i := 0; i < taskCount; i++ {
		iCopy := i
		pool.Execute(func() {
			t.Logf("Executing task %d ------> Thread: %v", iCopy, time.Now())
		})
	}
	pool.Shutdown()
	fmt.Println("All tasks executed.")
}