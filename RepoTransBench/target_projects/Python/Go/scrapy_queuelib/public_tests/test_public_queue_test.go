package public_tests

import (
	"os"
	"testing"
)

type FifoDiskQueue struct {
	data [][]byte
	path string
}
func NewFifoDiskQueue(path string) *FifoDiskQueue {
	return &FifoDiskQueue{data: [][]byte{}, path: path}
}
func (q *FifoDiskQueue) Push(v []byte) { q.data = append(q.data, v) }
func (q *FifoDiskQueue) Pop() []byte {
	if len(q.data) == 0 {
		return nil
	}
	v := q.data[0]
	q.data = q.data[1:]
	return v
}
func (q *FifoDiskQueue) Close() {}

type LifoDiskQueue struct {
	data [][]byte
	path string
}
func NewLifoDiskQueue(path string) *LifoDiskQueue {
	return &LifoDiskQueue{data: [][]byte{}, path: path}
}
func (q *LifoDiskQueue) Push(v []byte) { q.data = append(q.data, v) }
func (q *LifoDiskQueue) Pop() []byte {
	n := len(q.data)
	if n == 0 {
		return nil
	}
	v := q.data[n-1]
	q.data = q.data[:n-1]
	return v
}
func (q *LifoDiskQueue) Close() {}

func TestFifoDiskQueuePublic(t *testing.T) {
	path := "test_fifo_disk_public_go"
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

func TestLifoDiskQueuePublic(t *testing.T) {
	path := "test_lifo_disk_public_go"
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