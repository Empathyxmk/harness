package original

import (
	"testing"
	"container/heap"
	"github.com/stretchr/testify/assert"
)

// PriorityItem is a struct for holding an item with priority for heap
type PriorityItem struct {
	value    interface{}
	priority int
	index    int
}

// PriorityQueue implements heap.Interface and holds PriorityItems
type PriorityQueue []*PriorityItem

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the lowest priority number
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*PriorityItem)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	if n == 0 {
		return nil
	}
	item := old[n-1]
	*pq = old[0 : n-1]
	return item
}

type PQueue struct {
	items *PriorityQueue
}

func NewPQueue() *PQueue {
	pq := &PriorityQueue{}
	heap.Init(pq)
	return &PQueue{items: pq}
}

func (q *PQueue) Push(val interface{}, priority int) {
	heap.Push(q.items, &PriorityItem{
		value:    val,
		priority: priority,
	})
}

func (q *PQueue) Pop() interface{} {
	if q.items.Len() == 0 {
		return nil
	}
	item := heap.Pop(q.items)
	if item == nil {
		return nil
	}
	return item.(*PriorityItem).value
}

func (q *PQueue) Len() int {
	return q.items.Len()
}

func (q *PQueue) Close() error {
	return nil
}

func (q *PQueue) Open() error {
	return nil
}

func (q *PQueue) Sync() error {
	return nil
}

func TestPQueue_PushPopOrder(t *testing.T) {
	q := NewPQueue()
	q.Push("task3", 3)
	q.Push("task1", 1)
	q.Push("task5", 5)
	q.Push("task2", 2)
	q.Push("task4", 4)

	expected := []string{"task1", "task2", "task3", "task4", "task5"}
	for _, want := range expected {
		got := q.Pop()
		assert.Equal(t, want, got)
	}
	assert.Nil(t, q.Pop()) // Should be empty now
}

func TestPQueue_PriorityTie(t *testing.T) {
	q := NewPQueue()
	q.Push("a", 2)
	q.Push("b", 1)
	q.Push("c", 1)
	first := q.Pop()
	second := q.Pop()
	third := q.Pop()
	// Items with same priority could be popped in any order,
	// so we check they are present in the result
	assert.Contains(t, []string{first.(string), second.(string)}, "b")
	assert.Contains(t, []string{first.(string), second.(string)}, "c")
	assert.Equal(t, "a", third)
}

func TestPQueue_Len(t *testing.T) {
	q := NewPQueue()
	assert.Equal(t, 0, q.Len())
	q.Push("a", 2)
	q.Push("b", 1)
	assert.Equal(t, 2, q.Len())
	q.Pop()
	assert.Equal(t, 1, q.Len())
	q.Pop()
	assert.Equal(t, 0, q.Len())
}

func TestPQueue_CloseOpenSync(t *testing.T) {
	q := NewPQueue()
	assert.NoError(t, q.Close())
	assert.NoError(t, q.Open())
	assert.NoError(t, q.Sync())
}

func TestPQueue_EmptyPop(t *testing.T) {
	q := NewPQueue()
	assert.Nil(t, q.Pop())
	q.Push("x", 1)
	assert.Equal(t, "x", q.Pop())
	assert.Nil(t, q.Pop())
}