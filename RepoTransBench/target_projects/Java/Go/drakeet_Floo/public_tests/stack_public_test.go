package public_tests

import (
	"testing"
)

type Stack[T any] struct {
	data []T
}
func NewStack[T any]() *Stack[T] {
	return &Stack[T]{}
}
func (s *Stack[T]) Push(val T) {
	s.data = append(s.data, val)
}
func (s *Stack[T]) Pop() T {
	if len(s.data) == 0 {
		var zero T
		return zero
	}
	val := s.data[len(s.data)-1]
	s.data = s.data[:len(s.data)-1]
	return val
}
func (s *Stack[T]) IsEmpty() bool {
	return len(s.data) == 0
}

func TestPushThenPop_public(t *testing.T) {
	stack := NewStack[int]()
	stack.Push(99)
	stack.Push(42)
	r := stack.Pop()
	if r != 42 {
		t.Errorf("expected 42, got %v", r)
	}
	r2 := stack.Pop()
	if r2 != 99 {
		t.Errorf("expected 99, got %v", r2)
	}
}

func TestIsEmpty_public(t *testing.T) {
	stack := NewStack[int]()
	if !stack.IsEmpty() {
		t.Error("expected stack to be empty")
	}
	stack.Push(1)
	if stack.IsEmpty() {
		t.Error("expected stack to not be empty after push")
	}
}