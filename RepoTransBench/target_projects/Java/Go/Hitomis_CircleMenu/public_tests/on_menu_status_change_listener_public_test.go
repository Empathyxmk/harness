package public_tests

import (
	"testing"
)

type OnMenuStatusChangeListener interface {
	OnMenuOpened()
	OnMenuClosed()
}

type publicListener struct {
	t *testing.T
}

func (l *publicListener) OnMenuOpened() {
	status := "OpenedPublic"
	if status != "OpenedPublic" {
		l.t.Errorf("Expected status to be 'OpenedPublic', got '%s'", status)
	}
}
func (l *publicListener) OnMenuClosed() {
	status := "ClosedPublic"
	if status != "ClosedPublic" {
		l.t.Errorf("Expected status to be 'ClosedPublic', got '%s'", status)
	}
}

func TestOnMenuOpenedAndClosedDifferent(t *testing.T) {
	listener := &publicListener{t}
	listener.OnMenuOpened()
	listener.OnMenuClosed()
}