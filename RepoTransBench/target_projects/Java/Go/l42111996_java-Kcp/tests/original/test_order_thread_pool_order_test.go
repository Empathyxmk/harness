package original

import (
	"sort"
	"sync"
	"testing"
	"time"
)

// FakeOrderedTask is a struct to mimic an orderable task
type FakeOrderedTask struct {
	order int
	done  chan struct{}
}

func (t *FakeOrderedTask) Run(results *[]int, wg *sync.WaitGroup) {
	defer wg.Done()
	defer close(t.done)
	time.Sleep(time.Duration(t.order%3) * 10 * time.Millisecond)
	*results = append(*results, t.order)
}

type OrderedThreadPool struct {
	taskCh  chan *FakeOrderedTask
	wg      sync.WaitGroup
	results *[]int
	stop    chan struct{}
}

func NewOrderedThreadPool(results *[]int) *OrderedThreadPool {
	pool := &OrderedThreadPool{
		taskCh:  make(chan *FakeOrderedTask, 100),
		results: results,
		stop:    make(chan struct{}),
	}
	go pool.loop()
	return pool
}

func (p *OrderedThreadPool) loop() {
	for {
		select {
		case task := <-p.taskCh:
			p.wg.Add(1)
			task.Run(p.results, &p.wg)
		case <-p.stop:
			return
		}
	}
}

func (p *OrderedThreadPool) Submit(t *FakeOrderedTask) {
	p.taskCh <- t
}

func (p *OrderedThreadPool) Shutdown() {
	close(p.stop)
	p.wg.Wait()
}

func TestOrderedThreadPoolOrder(t *testing.T) {
	totalTasks := 20
	var results []int
	pool := NewOrderedThreadPool(&results)

	// Submit tasks with increasing order
	for i := 0; i < totalTasks; i++ {
		task := &FakeOrderedTask{order: i, done: make(chan struct{})}
		pool.Submit(task)
	}

	time.Sleep(500 * time.Millisecond) // Wait for all tasks to probably finish
	pool.Shutdown()

	// Validate all task orders exist and in correct sequence
	if len(results) != totalTasks {
		t.Errorf("Expected %d completed tasks, got %d", totalTasks, len(results))
	}
	for i, val := range results {
		if val != i {
			t.Errorf("Expected result order %d at index %d, got %d", i, i, val)
		}
	}
	// Also test that the slice is strictly increasing
	if !sort.IsSorted(sort.IntSlice(results)) {
		t.Errorf("Results are not in increasing order: %v", results)
	}
}