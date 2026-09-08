package original

import (
	"sync"
	"testing"
	"time"
)

type GoTrigger struct {
	lock  sync.Mutex
	value float64
	delay float64
}

func NewGoTrigger(delay float64) *GoTrigger {
	return &GoTrigger{
		delay: delay,
	}
}

func (t *GoTrigger) Emit() {
	t.lock.Lock()
	defer t.lock.Unlock()
	t.value = float64(time.Now().UnixNano())/1e9 + t.delay
}
func (t *GoTrigger) EmitNow() {
	t.lock.Lock()
	defer t.lock.Unlock()
	t.value = float64(time.Now().UnixNano())/1e9
}
func (t *GoTrigger) IsActive() bool {
	t.lock.Lock()
	defer t.lock.Unlock()
	return t.value != 0
}
func (t *GoTrigger) Release() {
	t.lock.Lock()
	defer t.lock.Unlock()
	t.value = 0
}
func (t *GoTrigger) Check() bool {
	t.lock.Lock()
	defer t.lock.Unlock()
	return t.value > 0 && float64(time.Now().UnixNano())/1e9 > t.value
}

func TestGoTriggerEmitActivatesAndCheck(t *testing.T) {
	tr := NewGoTrigger(0.02)
	if tr.IsActive() {
		t.Error("Should not be active at start")
	}
	tr.Emit()
	if !tr.IsActive() {
		t.Error("Should be active after Emit()")
	}
	time.Sleep(30 * time.Millisecond)
	if !tr.Check() {
		t.Error("Check should be true after delay")
	}
	tr.Release()
	if tr.IsActive() {
		t.Error("Should not be active after Release()")
	}
}

func TestGoTriggerEmitNowActivatesImmediately(t *testing.T) {
	tr := NewGoTrigger(10)
	tr.EmitNow()
	if !tr.IsActive() {
		t.Error("Should be active after EmitNow()")
	}
	tr.Release()
}

func TestGoTriggerCheckReturnsFalseIfNotReachedTime(t *testing.T) {
	// test that check is false if time has not reached
	tr := NewGoTrigger(0.2)
	tr.Emit()
	if tr.Check() {
		t.Error("Check should be false before time has elapsed")
	}
	tr.Release()
}

func TestGoTriggerConcurrentEmit(t *testing.T) {
	tr := NewGoTrigger(0.001)
	var wg sync.WaitGroup
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			tr.Emit()
			wg.Done()
		}()
	}
	wg.Wait()
	if !tr.IsActive() {
		t.Error("At least one Emit should make trigger active")
	}
	tr.Release()
}