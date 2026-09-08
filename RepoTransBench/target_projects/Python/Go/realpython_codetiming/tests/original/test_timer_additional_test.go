package original

import (
	"math"
	"testing"
	"time"
)

// Simulating Timer and TimerError as in test_codetiming_test.go

func TestTimerContextManagerRuns(t *testing.T) {
	timer := NewTimer("cmmsg", "Elapsed time: %.4fs")
	timer.Context(func(_ *Timer) {})
}

func TestTimerStartStopElapsed(t *testing.T) {
	timer := NewTimer("simple", "Time %.4f")
	if timer._startTime != nil {
		t.Errorf("Expected start time nil")
	}
	if err := timer.start(); err != nil {
		t.Fatalf("start failed: %v", err)
	}
	if timer._startTime == nil {
		t.Errorf("Expected start time not nil after start")
	}
	timer.stop()
	elapsed := timer.Last
	if _, ok := (interface{})(elapsed).(float64); !ok {
		t.Errorf("elapsed should be float64")
	}
}

func TestTimerStrRepr(t *testing.T) {
	timer := NewTimer("simple", "Time %.4f")
	s := timer.String()
	if s == "" {
		t.Error("String() should return non-empty string")
	}
	if !contains(timer.GoString(), "Timer") {
		t.Error("GoString() does not contain 'Timer'")
	}
}

func TestTimerRunningStatusViaPrivate(t *testing.T) {
	timer := NewTimer("runstat", "Running:%v")
	if err := timer.start(); err != nil {
		t.Fatal(err)
	}
	if timer._startTime == nil {
		t.Error("_start_time should not be nil when running")
	}
	timer.stop()
	if timer._startTime != nil {
		t.Error("_start_time should be nil after stop")
	}
}

func TestTimerLoggerCallableText(t *testing.T) {
	var messages []string
	cb := func(s string) { messages = append(messages, s) }
	timer := NewTimer("cbmsg", func(f float64) string { return "Time=" + formatFloat2(f) })
	timer._logger = cb
	timer.start()
	timer.stop()
	if len(messages) == 0 {
		t.Error("messages should not be empty")
	}
	found := false
	for _, m := range messages {
		if contains(m, "Time=") {
			found = true
		}
	}
	if !found {
		t.Error("Expected message to contain 'Time='")
	}
}

func TestTimerWithoutTextLogger(t *testing.T) {
	timer := NewTimer("notext", nil)
	timer._logger = nil
	timer.start()
	timer.stop()
}

func TestTimerStopWithoutStartRaises(t *testing.T) {
	timer := NewTimer("exception", "fail")
	_, err := timer.stop()
	if err == nil {
		t.Error("Expected error on stop before start")
	}
}

func TestTimerMultipleStartsRaises(t *testing.T) {
	timer := NewTimer("multi", "multi")
	timer.start()
	err := timer.start()
	if err == nil {
		t.Error("Expected error on multiple starts")
	}
	timer.stop()
}

func TestTimerLastWhenNan(t *testing.T) {
	timer := NewTimer("none", "none")
	if !math.IsNaN(timer.Last) {
		t.Errorf("Last should be NaN for new timer, got %v", timer.Last)
	}
}

func TestTimerCompareMultipleInstances(t *testing.T) {
	timer1 := NewTimer("a", nil)
	timer2 := NewTimer("b", nil)
	if timer1 == timer2 {
		t.Error("timer1 and timer2 should not be same instance")
	}
}

// --- Utility functions used by tests

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (substr == "" || (len(s) > 0 && len(substr) > 0 && (len(s) == len(substr) || (len(s) > len(substr) && (s[0:len(substr)] == substr || contains(s[1:], substr)))))
}

func formatFloat2(f float64) string {
	return fmt.Sprintf("%.2f", f)
}