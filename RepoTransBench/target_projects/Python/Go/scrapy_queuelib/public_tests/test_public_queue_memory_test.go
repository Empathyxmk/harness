package public_tests

import (
	"testing"
)

// Dummy BaseQueue to match isinstance/issubclass checks
type BaseQueue interface {
	Push(obj interface{})
	Pop() interface{}
	Peek() interface{}
	Close()
	Len() int
}

type AnotherDummyQueue struct{}

func (d *AnotherDummyQueue) Push(obj interface{}) {}
func (d *AnotherDummyQueue) Pop() interface{}     { return nil }
func (d *AnotherDummyQueue) Peek() interface{}    { return nil }
func (d *AnotherDummyQueue) Close()               {}
func (d *AnotherDummyQueue) Len() int             { return 0 }

func TestInstanceAndSubclassPublic(t *testing.T) {
	// Go doesn't have isinstance/issubclass, but type conformance can be checked.
	var bq BaseQueue = &AnotherDummyQueue{}
	if bq == nil {
		t.Error("AnotherDummyQueue should implement BaseQueue interface")
	}
	// No runtime subclassing in Go; types must implement interfaces.
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

func TestFifoMemoryQueuePublic(t *testing.T) {
	q := NewFifoMemoryQueue()
	if got := q.Len(); got != 0 {
		t.Errorf("expected len(q) == 0, got %d", got)
	}
	q.Push(100)
	q.Push(200)
	q.Push(300)
	if got := q.Len(); got != 3 {
		t.Errorf("expected len(q) == 3, got %d", got)
	}
	if got := q.Peek(); got != 100 {
		t.Errorf("Peek() == %v, want 100", got)
	}
	if got := q.Pop(); got != 100 {
		t.Errorf("Pop() == %v, want 100", got)
	}
	if got := q.Peek(); got != 200 {
		t.Errorf("Peek() == %v, want 200", got)
	}
	if got := q.Pop(); got != 200 {
		t.Errorf("Pop() == %v, want 200", got)
	}
	if got := q.Peek(); got != 300 {
		t.Errorf("Peek() == %v, want 300", got)
	}
	if got := q.Pop(); got != 300 {
		t.Errorf("Pop() == %v, want 300", got)
	}
	if got := q.Peek(); got != nil {
		t.Errorf("Peek() after empty == %v, want nil", got)
	}
	if got := q.Pop(); got != nil {
		t.Errorf("Pop() after empty == %v, want nil", got)
	}
	q.Close()
}

func TestFifoMemoryQueueEmptyBehaviourPublic(t *testing.T) {
	q := NewFifoMemoryQueue()
	if q.Peek() != nil {
		t.Errorf("Peek() on empty should be nil, got %v", q.Peek())
	}
	if q.Pop() != nil {
		t.Errorf("Pop() on empty should be nil, got %v", q.Pop())
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

func TestLifoMemoryQueuePublic(t *testing.T) {
	q := NewLifoMemoryQueue()
	if got := q.Len(); got != 0 {
		t.Errorf("expected len(q) == 0, got %d", got)
	}
	q.Push("x")
	q.Push("y")
	q.Push("z")
	if got := q.Len(); got != 3 {
		t.Errorf("expected len(q) == 3, got %d", got)
	}
	if got := q.Peek(); got != "z" {
		t.Errorf("Peek() == %v, want z", got)
	}
	if got := q.Pop(); got != "z" {
		t.Errorf("Pop() == %v, want z", got)
	}
	if got := q.Peek(); got != "y" {
		t.Errorf("Peek() == %v, want y", got)
	}
	if got := q.Pop(); got != "y" {
		t.Errorf("Pop() == %v, want y", got)
	}
	if got := q.Peek(); got != "x" {
		t.Errorf("Peek() == %v, want x", got)
	}
	if got := q.Pop(); got != "x" {
		t.Errorf("Pop() == %v, want x", got)
	}
	if got := q.Peek(); got != nil {
		t.Errorf("Peek() after empty == %v, want nil", got)
	}
	if got := q.Pop(); got != nil {
		t.Errorf("Pop() after empty == %v, want nil", got)
	}
	q.Close()
}