package original

import (
	"container/heap"
	"testing"
)

// PriorityQueue implementation for testing
type IntHeap []interface{}

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool {
	// Numbers should compare as float64 if at least one is float, otherwise int
	a, b := h[i], h[j]
	af, aok := a.(float64)
	bf, bok := b.(float64)
	if aok && bok {
		return af < bf
	} else if aok {
		return af < float64(b.(int))
	} else if bok {
		return float64(a.(int)) < bf
	} else {
		return a.(int) < b.(int)
	}
}
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *IntHeap) Push(x interface{}) { *h = append(*h, x) }
func (h *IntHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func TestPriorityQueueBasicFunctionality(t *testing.T) {
	queue := &IntHeap{}
	heap.Init(queue)

	if queue.Len() != 0 {
		t.Errorf("Expected queue to be empty at start")
	}
	heap.Push(queue, 0)
	heap.Push(queue, 3.14159)
	heap.Push(queue, 3)
	heap.Push(queue, 1)
	heap.Push(queue, 6)
	heap.Push(queue, -21)
	heap.Push(queue, 0)

	if queue.Len() == 0 {
		t.Errorf("Expected queue to not be empty after puts")
	}

	vals := make([]interface{}, 0, 7)
	for queue.Len() > 0 {
		vals = append(vals, heap.Pop(queue))
	}

	// expect sorted: -21, 0, 0, 1, 3, 3.14159, 6
	exp := []interface{}{-21, 0, 0, 1, 3, 3.14159, 6}
	for i := range vals {
		if vals[i] != exp[i] {
			t.Errorf("expected %v at idx %d, got %v", exp[i], i, vals[i])
		}
	}

	if len(vals) != 7 {
		t.Errorf("Expected 7 elements, got %d", len(vals))
	}
}

func TestUniqueQueueBasicFunctionality(t *testing.T) {
	type UniqueQueue struct {
		elems       []int
		seen        map[int]bool
		silent      bool
		explicitUnsee bool
	}
	Duplicate := struct{}{}

	var q UniqueQueue
	q.seen = make(map[int]bool)

	put := func(val int) error {
		if q.seen[val] {
			if q.silent {
				return nil
			} else {
				return &Duplicate
			}
		}
		q.elems = append(q.elems, val)
		q.seen[val] = true
		return nil
	}
	get := func() int {
		val := q.elems[0]
		q.elems = q.elems[1:]
		if q.explicitUnsee {
			// don't unsee automatically
		} else {
			delete(q.seen, val)
		}
		return val
	}
	unsee := func(val int) {
		delete(q.seen, val)
	}

	q.silent = true
	put(2)
	put(0)
	put(2)
	put(1)

	q.silent = false
	if err := put(0); err == nil {
		t.Errorf("Expected Duplicate error when putting dupe with silent=false")
	}

	if len(q.elems) == 0 {
		t.Errorf("Expected not empty after puts")
	}
	// Remove stuff
	if v := get(); v != 2 {
		t.Errorf("Expect get 2 first, got %v", v)
	}
	if v := get(); v != 0 {
		t.Errorf("Expect get 0 second, got %v", v)
	}
	if v := get(); v != 1 {
		t.Errorf("Expect get 1 third, got %v", v)
	}
	if len(q.elems) != 0 {
		t.Errorf("Should be empty after all gets")
	}

	// Put an old duplicate back
	put(0)
	if len(q.elems) == 0 {
		t.Errorf("Expected not empty with re-put")
	}
	q.silent = true
	q.explicitUnsee = true
	get()
	if len(q.elems) != 0 {
		t.Errorf("Expected empty after remove with explicit")
	}
	put(0)
	if len(q.elems) != 0 {
		t.Errorf("Should be empty if item was not unseen")
	}
	unsee(0)
	put(0)
	if len(q.elems) != 1 {
		t.Errorf("Should not be empty after proper unsee and re-put")
	}
}