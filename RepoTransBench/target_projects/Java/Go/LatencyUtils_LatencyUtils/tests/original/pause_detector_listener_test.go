package tests

import (
	"testing"
)

type testListener struct {
	receivedLength int64
	receivedTime   int64
}

func (l *testListener) HandlePauseEvent(pauseLength, pauseEndTime int64) {
	l.receivedLength = pauseLength
	l.receivedTime = pauseEndTime
}

func TestPauseEventIsHandledCorrectly(t *testing.T) {
	listener := &testListener{}
	listener.HandlePauseEvent(555, 999)
	if listener.receivedLength != 555 {
		t.Errorf("receivedLength should be 555, got %d", listener.receivedLength)
	}
	if listener.receivedTime != 999 {
		t.Errorf("receivedTime should be 999, got %d", listener.receivedTime)
	}
}