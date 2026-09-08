package public_tests

import (
	"math"
	"testing"
	"time"
)

func TestTimerContextManagerRunsPublic(t *testing.T) {
	timer := NewTimer("public_cmmsg", "Public elapsed: %.6fs")
	timer.Context(func(_ *Timer) {})
}

func TestTimerStartStopElapsedPublic(t *testing.T) {
	timer := NewTimer("public_simple", "Duration %.2f")
	if timer._startTime != nil {
		t.Errorf("expected nil start_time")
	}
	if err := timer.start(); err != nil {
		t.Fatal("error starting timer:", err)
	}
	if timer._startTime == nil {
		t.Errorf("expected start_time not nil")
	}
	timer.stop()
	elapsed := timer.Last
	if _, ok := (interface{})(elapsed).(float64); !ok {
		t.Errorf("elapsed is not float64")
	}
	if elapsed < 0.0 {
		t.Errorf("elapsed < 0.0")
	}
}

func TestTimerStrReprPublic(t *testing.T) {
	timer := NewTimer("public_simple", "Duration %.2f")
	s := timer.String()
	if s == "" {
		t.Error("String() should not be empty")
	}
}

func TestTimerRunningStatusViaPrivatePublic(t *testing.T) {
	timer := NewTimer("public_runstat", "Now running:%v")
	timer.start()
	if timer._startTime == nil {
		t.Error("_start_time should not be nil")
	}
	timer.stop()
	if timer._startTime != nil {
		t.Error("_start_time should be nil after stop")
	}
}

func TestTimerLoggerCallableTextPublic(t *testing.T) {
	var messages []string
	cb := func(msg string) { messages = append(messages, msg) }
	timer := NewTimer("public_cbmsg", "Elapsed=%.3f")
	timer._logger = cb
	timer.start()
	timer.stop()
	found := false
	for _, m := range messages {
		if len(m) > 0 && m[:7] == "Elapsed" {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected message to contain 'Elapsed='")
	}
}

func TestTimerWithoutTextLoggerPublic(t *testing.T) {
	timer := NewTimer("public_notext", nil)
	timer._logger = nil
	timer.start()
	timer.stop()
}

func TestTimerStopWithoutStartRaisesPublic(t *testing.T) {
	timer := NewTimer("public_exception", "fail fast")
	_, err := timer.stop()
	if err == nil {
		t.Error("Expected error on stop before start")
	}
}

func TestTimerMultipleStartsRaisesPublic(t *testing.T) {
	timer := NewTimer("public_multi", "multi-case")
	timer.start()
	err := timer.start()
	if err == nil {
		t.Error("Expected error on multiple starts")
	}
	timer.stop()
}

func TestTimerLastWhenNanPublic(t *testing.T) {
	timer := NewTimer("public_none", "noneCase")
	if !math.IsNaN(timer.Last) {
		t.Errorf("Last should be NaN, got %v", timer.Last)
	}
}

func TestTimerCompareMultipleInstancesPublic(t *testing.T) {
	timer1 := NewTimer("public_x", nil)
	timer2 := NewTimer("public_y", nil)
	if timer1 == timer2 {
		t.Error("timer1 and timer2 should be different instances")
	}
}