package public_tests

import (
	"testing"
)

type Trigger struct {
	IsRunning bool
}

func (t *Trigger) Toggle() {
	t.IsRunning = !t.IsRunning
}
func (t *Trigger) Pause() { t.IsRunning = false }
func (t *Trigger) Resume() { t.IsRunning = true }

func (t *Trigger) String() string {
	return "Trigger"
}

func TestTriggerToggleAndStr(t *testing.T) {
	trig := &Trigger{}
	trig.Toggle()
	if &trig.IsRunning == nil {
		t.Errorf("IsRunning should not be nil")
	}
	if trig.String() != "Trigger" {
		t.Errorf("String() should return Trigger")
	}
}

func TestTriggerPauseResume(t *testing.T) {
	trig := &Trigger{}
	trig.Pause()
	if trig.IsRunning != false {
		t.Errorf("Trigger should be paused")
	}
	trig.Resume()
	if trig.IsRunning != true {
		t.Errorf("Trigger should be running")
	}
}