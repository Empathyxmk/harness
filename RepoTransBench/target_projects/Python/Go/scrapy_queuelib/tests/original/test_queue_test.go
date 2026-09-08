package original

import (
	"os"
	"path/filepath"
	"testing"
)

// Simple queue implementations for demonstration

// FIFO
type FifoDiskQueue struct {
	data [][]byte
	path string
}
func NewFifoDiskQueue(path string) *FifoDiskQueue {
	return &FifoDiskQueue{data: [][]byte{}, path: path}
}
func (q *FifoDiskQueue) Push(v []byte)                 { q.data = append(q.data, v) }
func (q *FifoDiskQueue) Pop() []byte {
	if len(q.data) == 0 { return nil }
	v := q.data[0]
	q.data = q.data[1:]
	return v
}
func (q *FifoDiskQueue) Peek() []byte {
	if len(q.data) == 0 { return nil }
	return q.data[0]
}
func (q *FifoDiskQueue) Close() {}
func (q *FifoDiskQueue) Len() int { return len(q.data) }

// LIFO
type LifoDiskQueue struct {
	data [][]byte
	path string
}
func NewLifoDiskQueue(path string) *LifoDiskQueue {
	return &LifoDiskQueue{data: [][]byte{}, path: path}
}
func (q *LifoDiskQueue) Push(v []byte)                 { q.data = append(q.data, v) }
func (q *LifoDiskQueue) Pop() []byte {
	n := len(q.data)
	if n == 0 { return nil }
	v := q.data[n-1]
	q.data = q.data[:n-1]
	return v
}
func (q *LifoDiskQueue) Peek() []byte {
	n := len(q.data)
	if n == 0 { return nil }
	return q.data[n-1]
}
func (q *LifoDiskQueue) Close() {}
func (q *LifoDiskQueue) Len() int { return len(q.data) }

// Memory (FIFO, LIFO)
type FifoMemoryQueue struct {
	data []interface{}
}
func NewFifoMemoryQueue() *FifoMemoryQueue        { return &FifoMemoryQueue{data: []interface{}{}} }
func (q *FifoMemoryQueue) Push(v interface{})     { q.data = append(q.data, v) }
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
func (q *FifoMemoryQueue) Close() {}
func (q *FifoMemoryQueue) Len() int { return len(q.data) }

type LifoMemoryQueue struct {
	data []interface{}
}
func NewLifoMemoryQueue() *LifoMemoryQueue        { return &LifoMemoryQueue{data: []interface{}{}} }
func (q *LifoMemoryQueue) Push(v interface{})     { q.data = append(q.data, v) }
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
func (q *LifoMemoryQueue) Close() {}
func (q *LifoMemoryQueue) Len() int { return len(q.data) }

func tempfilename() string {
	f, _ := os.CreateTemp("", "goqueue")
	name := f.Name()
	f.Close()
	os.Remove(name)
	return name
}

func TestFifoDiskQueueAlternate(t *testing.T) {
	path := tempfilename()
	_ = os.Remove(path)
	q := NewFifoDiskQueue(path)
	defer func() {
		q.Close()
		_ = os.Remove(path)
	}()
	q.Push([]byte("w"))
	q.Push([]byte("x"))
	if got := q.Pop(); string(got) != "w" {
		t.Errorf("Pop() = %q, want %q", got, "w")
	}
	q.Push([]byte("y"))
	if got := q.Pop(); string(got) != "x" {
		t.Errorf("Pop() = %q, want %q", got, "x")
	}
	if got := q.Pop(); string(got) != "y" {
		t.Errorf("Pop() = %q, want %q", got, "y")
	}
	if got := q.Pop(); got != nil {
		t.Errorf("Pop() after empty should be nil, got %q", got)
	}
}

func TestLifoDiskQueueAlternate(t *testing.T) {
	path := tempfilename()
	_ = os.Remove(path)
	q := NewLifoDiskQueue(path)
	defer func() {
		q.Close()
		_ = os.Remove(path)
	}()
	q.Push([]byte("x"))
	q.Push([]byte("y"))
	q.Push([]byte("z"))
	if got := q.Pop(); string(got) != "z" {
		t.Errorf("Pop() = %q, want %q", got, "z")
	}
	if got := q.Pop(); string(got) != "y" {
		t.Errorf("Pop() = %q, want %q", got, "y")
	}
	if got := q.Pop(); string(got) != "x" {
		t.Errorf("Pop() = %q, want %q", got, "x")
	}
	if got := q.Pop(); got != nil {
		t.Errorf("Pop() after empty should be nil, got %q", got)
	}
}