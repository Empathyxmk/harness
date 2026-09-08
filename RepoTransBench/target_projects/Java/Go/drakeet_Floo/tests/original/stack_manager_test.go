package original

import "testing"

type Stack struct{}
type StackManager struct {
	stack []*Stack
}

func NewStackManager() *StackManager {
	return &StackManager{stack: []*Stack{}}
}

func (m *StackManager) Push(s *Stack) {
	m.stack = append(m.stack, s)
}

func (m *StackManager) Pop() *Stack {
	if len(m.stack) == 0 {
		return nil
	}
	s := m.stack[len(m.stack)-1]
	m.stack = m.stack[:len(m.stack)-1]
	return s
}

func (m *StackManager) Peek() *Stack {
	if len(m.stack) == 0 {
		return nil
	}
	return m.stack[len(m.stack)-1]
}

func (m *StackManager) IsNotEmpty() bool {
	return len(m.stack) > 0
}

func TestPushAndPeek(t *testing.T) {
	m := NewStackManager()
	s := &Stack{}
	m.Push(s)
	if m.Peek() != s {
		t.Error("Peek did not return pushed stack")
	}
}

func TestPopAndEmpty(t *testing.T) {
	m := NewStackManager()
	s := &Stack{}
	m.Push(s)
	popped := m.Pop()
	if popped != s {
		t.Error("Pop did not return correct stack")
	}
	if m.Peek() != nil {
		t.Error("Peek after pop should be nil")
	}
}

func TestEmptyPop(t *testing.T) {
	m := NewStackManager()
	if m.Pop() != nil {
		t.Error("Pop on empty should return nil")
	}
}

func TestIsNotEmpty(t *testing.T) {
	m := NewStackManager()
	if m.IsNotEmpty() {
		t.Error("Should not be not empty when empty")
	}
	m.Push(&Stack{})
	if !m.IsNotEmpty() {
		t.Error("Should be not empty after push")
	}
}