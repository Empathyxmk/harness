package public_tests

import (
	"testing"
)

type PhotoLoadListenerPublic interface {
	OnPhotoLoaded(count int)
}

type DummyListenerPublic struct {
	LastCount int
	Called    bool
}

func (l *DummyListenerPublic) OnPhotoLoaded(count int) {
	l.LastCount = count
	l.Called = true
}

func TestPhotoLoadListener_WithDifferentCount(t *testing.T) {
	listener := &DummyListenerPublic{}
	listener.OnPhotoLoaded(7)
	if !listener.Called {
		t.Error("OnPhotoLoaded should be called (public)")
	}
	if listener.LastCount != 7 {
		t.Errorf("Expected count 7, got %d", listener.LastCount)
	}
}

func TestPhotoLoadListener_MultipleCalls(t *testing.T) {
	listener := &DummyListenerPublic{}
	listener.OnPhotoLoaded(2)
	if !listener.Called {
		t.Error("OnPhotoLoaded should be called (public)")
	}
	if listener.LastCount != 2 {
		t.Errorf("Expected count 2, got %d", listener.LastCount)
	}
	listener.OnPhotoLoaded(12)
	if listener.LastCount != 12 {
		t.Errorf("Expected count 12, got %d", listener.LastCount)
	}
}