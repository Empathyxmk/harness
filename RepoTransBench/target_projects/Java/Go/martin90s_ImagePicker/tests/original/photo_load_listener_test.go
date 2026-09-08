package original

import (
	"testing"
)

type PhotoLoadListener interface {
	OnLoadComplete()
	OnLoadError()
}

type DummyListener struct {
	OnLoadCompleteCalled bool
	OnLoadErrorCalled    bool
}

func (l *DummyListener) OnLoadComplete() {
	l.OnLoadCompleteCalled = true
}
func (l *DummyListener) OnLoadError() {
	l.OnLoadErrorCalled = true
}

func TestPhotoLoadListenerListener(t *testing.T) {
	listener := &DummyListener{}
	listener.OnLoadComplete()
	listener.OnLoadError()
	if !listener.OnLoadCompleteCalled {
		t.Error("OnLoadComplete should be called")
	}
	if !listener.OnLoadErrorCalled {
		t.Error("OnLoadError should be called")
	}
}