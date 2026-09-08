package public_tests

import (
	"testing"
)

type OnMenuSelectedListener interface {
	OnMenuSelected(index int)
}

type onMenuSelectedPublic struct {
	t *testing.T
}

func (l *onMenuSelectedPublic) OnMenuSelected(index int) {
	if index != 2 {
		l.t.Errorf("Expected index to be 2, got %d", index)
	}
}

func TestOnMenuSelectedWithDifferentIndex(t *testing.T) {
	listener := &onMenuSelectedPublic{t}
	listener.OnMenuSelected(2)
}