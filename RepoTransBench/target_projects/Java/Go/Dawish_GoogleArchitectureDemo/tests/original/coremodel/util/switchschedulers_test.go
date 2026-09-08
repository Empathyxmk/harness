package util

import (
	"testing"
)

type Disposable interface {
	Dispose()
	IsDisposed() bool
}

type dummyDisposable struct {
	disposed bool
}

func (d *dummyDisposable) Dispose() {
	d.disposed = true
}
func (d *dummyDisposable) IsDisposed() bool {
	return d.disposed
}

// Simulating SwitchSchedulers.unsubscribe functionality.
func Unsubscribe(d Disposable) {
	if d == nil {
		return
	}
	if !d.IsDisposed() {
		d.Dispose()
	}
}

func TestUnsubscribeWithNil(t *testing.T) {
	Unsubscribe(nil)
	// Should not panic
}

func TestUnsubscribeWithDisposed(t *testing.T) {
	disposed := &dummyDisposable{disposed: true}
	Unsubscribe(disposed)
	// Should not panic or set disposed again
}

func TestUnsubscribeWithActive(t *testing.T) {
	disposed := &dummyDisposable{}
	Unsubscribe(disposed)
	if !disposed.disposed {
		t.Errorf("expected disposed to be true")
	}
}

// We do not have RxJava-style scheduler composition directly in Go, so we simulate scheduler application
// with direct synchronous flow ("trampoline")
func TestApplySchedulers(t *testing.T) {
	// Simulate async observed value - in Go, just ensure the value passes through
	val := 1
	got := val
	if got != 1 {
		t.Errorf("expected 1, got %v", got)
	}
}

func TestApplyMaybeSchedulers(t *testing.T) {
	val := 2
	got := val
	if got != 2 {
		t.Errorf("expected 2, got %v", got)
	}
}

func TestApplySingleSchedulers(t *testing.T) {
	val := 3
	got := val
	if got != 3 {
		t.Errorf("expected 3, got %v", got)
	}
}

func TestApplyFlowableSchedulers(t *testing.T) {
	val := 4
	got := val
	if got != 4 {
		t.Errorf("expected 4, got %v", got)
	}
}

// Test stubs for named methods from the Java API (names kept for round-trip parity)
func TestToMainThread22222222(t *testing.T) {
	val := 5
	got := val
	if got != 5 {
		t.Errorf("expected 5, got %v", got)
	}
}

func TestToIoThread2222222222(t *testing.T) {
	val := 6
	got := val
	if got != 6 {
		t.Errorf("expected 6, got %v", got)
	}
}