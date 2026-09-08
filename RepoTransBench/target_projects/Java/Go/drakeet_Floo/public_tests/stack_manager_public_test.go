package public_tests

import (
	"testing"
)

type StackManager[T any] struct {
	stack []T
}
func NewStackManager[T any]() *StackManager[T] {
	return &StackManager[T]{}
}
func (m *StackManager[T]) Push(val T) {
	m.stack = append(m.stack, val)
}
func (m *StackManager[T]) Pop() *T {
	if len(m.stack) == 0 {
		return nil
	}
	v := m.stack[len(m.stack)-1]
	m.stack = m.stack[:len(m.stack)-1]
	return &v
}

func TestPushPop_public(t *testing.T) {
	m := NewStackManager[string]()
	m.Push("alpha")
	m.Push("beta")
	if got := m.Pop(); got == nil || *got != "beta" {
		t.Errorf("expected 'beta', got %v", got)
	}
	if got := m.Pop(); got == nil || *got != "alpha" {
		t.Errorf("expected 'alpha', got %v", got)
	}
}

func TestPopOnEmpty_public(t *testing.T) {
	m := NewStackManager[string]()
	if got := m.Pop(); got != nil {
		t.Error("expected nil on Pop for empty stack")
	}
}