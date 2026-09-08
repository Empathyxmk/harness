package original

import (
	"testing"
)

type OnMenuSelectedListener interface {
	OnMenuSelected(index int)
}

type MenuSelectedListener struct {
	LastSelectedIndex int
}

func (l *MenuSelectedListener) OnMenuSelected(index int) {
	l.LastSelectedIndex = index
}

func TestOnMenuSelectedCalled(t *testing.T) {
	listener := &MenuSelectedListener{LastSelectedIndex: -1}
	listener.OnMenuSelected(2)
	if listener.LastSelectedIndex != 2 {
		t.Errorf("Expected LastSelectedIndex to be 2, got %d", listener.LastSelectedIndex)
	}
	listener.OnMenuSelected(0)
	if listener.LastSelectedIndex != 0 {
		t.Errorf("Expected LastSelectedIndex to be 0, got %d", listener.LastSelectedIndex)
	}
}