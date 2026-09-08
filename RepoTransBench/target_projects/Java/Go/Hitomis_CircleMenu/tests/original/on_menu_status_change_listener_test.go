package original

import (
	"testing"
)

type OnMenuStatusChangeListener interface {
	OnMenuOpened()
	OnMenuClosed()
}

type StatusListener struct {
	Opened bool
	Closed bool
}

func (l *StatusListener) OnMenuOpened() {
	l.Opened = true
}
func (l *StatusListener) OnMenuClosed() {
	l.Closed = true
}

func TestOnMenuOpenedAndClosed(t *testing.T) {
	listener := &StatusListener{}
	if listener.Opened {
		t.Error("Initially opened should be false")
	}
	if listener.Closed {
		t.Error("Initially closed should be false")
	}
	listener.OnMenuOpened()
	if !listener.Opened {
		t.Error("After OnMenuOpened, opened should be true")
	}
	listener.OnMenuClosed()
	if !listener.Closed {
		t.Error("After OnMenuClosed, closed should be true")
	}
}