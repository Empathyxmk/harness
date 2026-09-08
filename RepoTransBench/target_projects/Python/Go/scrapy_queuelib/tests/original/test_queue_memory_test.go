package original

import (
	"testing"
)

// Dummy BaseQueue to match interface
type BaseQueue interface {
	Push(obj interface{})
	Pop() interface{}
	Peek() interface{}
	Close()
	Len() int
}
type DummyQueue struct{}
func (DummyQueue) Push(obj interface{})       {}
func (DummyQueue) Pop() interface{}           { return nil }
func (DummyQueue) Peek() interface{}          { return nil }
func (DummyQueue) Close()                     {}
func (DummyQueue) Len() int                   { return 0 }

func TestInstanceCheckAndSubclassCheck(t *testing.T) {
	var bq BaseQueue = DummyQueue{}
	if bq == nil {
		t.Error("DummyQueue should implement BaseQueue interface")
	}
}

type FifoMemoryQueue struct {
	data []interface{}
}
func NewFifoMemoryQueue() *FifoMemoryQueue { return &FifoMemoryQueue{data: []interface{}{}} }
func (q *FifoMemoryQueue) Push(v interface{}) { q.data = append(q.data, v) }
func (q *FifoMemoryQueue) Pop() interface{} {
	if len(q.data) == 0 { return nil }
	v := q.data[0]
	q.data = q.data[1:]
	return v
}
func (q *FifoMemoryQueue) Peek() interface{} {
	if len(q.data) == 0 { return nil }
	return q.data[0]
}
func (q *FifoMemoryQueue) Len() int { return len(q.data) }
func (q *FifoMemoryQueue) Close()   {}

func TestFifoNormal(t *testing.T) {
	q := NewFifoMemoryQueue()
	if got := q.Len(); got != 0 {
		t.Errorf("expected len(q) == 0, got %d", got)
	}
	q.Push(1)
	q.Push(2)
	if got := q.Len(); got != 2 {
		t.Errorf("expected len(q) == 2, got %d", got)
	}
	if got := q.Peek(); got != 1 {
		t.Errorf("Peek() == %v, want 1", got)
	}
	if got := q.Pop(); got != 1 {
		t.Errorf("Pop() == %v, want 1", got)
	}
	if got := q.Peek(); got != 2 {
		t.Errorf("Peek() == %v, want 2", got)
	}
	if got := q.Pop(); got != 2 {
		t.Errorf("Pop() == %v, want 2", got)
	}
	if got := q.Peek(); got != nil {
		t.Errorf("Peek() after empty == %v, want nil", got)
	}
	if got := q.Pop(); got != nil {
		t.Errorf("Pop() after empty == %v, want nil", got)
	}
	q.Close()
}

func TestFifoEmptyPopPeek(t *testing.T) {
	q := NewFifoMemoryQueue()
	if q.Pop() != nil {
		t.Errorf("Pop() on empty must be nil")
	}
	if q.Peek() != nil {
		t.Errorf("Peek() on empty must be nil")
	}
	q.Close()
}

type LifoMemoryQueue struct {
	data []interface{}
}
func NewLifoMemoryQueue() *LifoMemoryQueue { return &LifoMemoryQueue{data: []interface{}{}} }
func (q *LifoMemoryQueue) Push(v interface{}) { q.data = append(q.data, v) }
func (q *LifoMemoryQueue) Pop() interface{} {
	n := len(q.data)
	if n == 0 { return nil }
	v := q.data[n-1]
	q.data = q.data[:n-1]
	return v
}
func (q *LifoMemoryQueue) Peek() interface{} {
	n := len(q.data)
	if n == 0 { return nil }
	return q.data[n-1]
}
func (q *LifoMemoryQueue) Len() int { return len(q.data) }
func (q *LifoMemoryQueue) Close()   {}

func TestLifoNormal(t *testing.T) {
	q := NewLifoMemoryQueue()
	if got := q.Len(); got != 0 {
		t.Errorf("expected len(q) == 0, got %d", got)
	}
	q.Push("a")
	q.Push("b")
	if got := q.Len(); got != 2 {
		t.Errorf("expected len(q) == 2, got %d", got)
	}
	if got := q.Peek(); got != "b" {
		t.Errorf("Peek() == %v, want b", got)
	}
	if got := q.Pop(); got != "b" {
		t.Errorf("Pop() == %v, want b", got)
	}
	if got := q.Peek(); got != "a" {
		t.Errorf("Peek() == %v, want a", got)
	}
	if got := q.Pop(); got != "a" {
		t.Errorf("Pop() == %v, want a", got)
	}
	if got := q.Peek(); got != nil {
		t.Errorf("Peek() after empty == %v, want nil", got)
	}
	if got := q.Pop(); got != nil {
		t.Errorf("Pop() after empty == %v, want nil", got)
	}
	q.Close()
}