package public_tests

import (
	"testing"
)

type ListenerPublic struct {
	wasCalled *bool
}

func (l *ListenerPublic) HandlePauseEvent(pauseLength, pauseEndTime int64) {
	if pauseLength == 777 && pauseEndTime == 5555 {
		*l.wasCalled = true
	}
}

func TestListenerIsCalledWithDifferentArgs(t *testing.T) {
	wasCalled := false
	l := &ListenerPublic{wasCalled: &wasCalled}
	l.HandlePauseEvent(777, 5555)
	if !wasCalled {
		t.Errorf("Listener was not called with expected arguments")
	}
}