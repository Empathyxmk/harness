package public_tests

import (
	"bytes"
	"math"
	"regexp"
	"strings"
	"testing"
	"time"
)

func mustMatchRE(t *testing.T, re string, s string) {
	t.Helper()
	if matched, err := regexp.MatchString(re, s); err != nil || !matched {
		t.Fatalf("pattern %q did not match %q", re, s)
	}
}

// Simulate Timer and TimerError for public tests.
type TimerError struct{ Message string }
func (e TimerError) Error() string { return e.Message }

type Timer struct {
	Name        string
	Text        interface{}
	Last        float64
	InitialText interface{}
	_logger     func(string)
	_startTime  *time.Time
}

func NewTimer(name string, text interface{}) *Timer {
	return &Timer{Name: name, Text: text, Last: math.NaN(), _logger: func(string) {}}
}

func (t *Timer) start() error {
	if t._startTime != nil {
		return TimerError{"timer already started"}
	}
	now := time.Now()
	t._startTime = &now
	return nil
}

func (t *Timer) stop() (float64, error) {
	if t._startTime == nil {
		return 0, TimerError{"timer not running"}
	}
	elapsed := time.Since(*t._startTime).Seconds()
	t.Last = elapsed
	t._startTime = nil
	return elapsed, nil
}

func (t *Timer) Context(f func(*Timer)) {
	t.start()
	f(t)
	t.stop()
}

var USER_TIME_PREFIX = "Time spent:"
var USER_TIME_MESSAGE = USER_TIME_PREFIX + " %.5f s"
var RE_USER_TIME_MESSAGE = USER_TIME_PREFIX + ` 0\.\d{5} s`

type MyLogger struct{ logs string }
func (l *MyLogger) Print(msg string) { l.logs += msg }
func (l *MyLogger) Log(msg string)   { l.Print(msg) }

func wasteCustomTime(num int) {
	x := 0
	for n := 0; n < num; n++ {
		x += n + 1
	}
	_ = x
}

func TestTimerAsContextManagerPublic(t *testing.T) {
	var buf bytes.Buffer
	timer := NewTimer("", USER_TIME_MESSAGE)
	timer._logger = func(msg string) { buf.WriteString(msg + "\n") }
	timer.Context(func(_ *Timer) { wasteCustomTime(500) })
	mustMatchRE(t, RE_USER_TIME_MESSAGE, buf.String())
	if strings.Count(buf.String(), "\n") != 1 {
		t.Error("should be 1 newline in timing output")
	}
}

func TestExplicitTimerPublic(t *testing.T) {
	var buf bytes.Buffer
	timer := NewTimer("", USER_TIME_MESSAGE)
	timer._logger = func(msg string) { buf.WriteString(msg + "\n") }
	em := timer.start()
	if em != nil {
		t.Fatalf("unexpected error: %v", em)
	}
	wasteCustomTime(500)
	timer.stop()
	mustMatchRE(t, RE_USER_TIME_MESSAGE, buf.String())
	if strings.Count(buf.String(), "\n") != 1 {
		t.Error("should be 1 newline in timing output")
	}
}

func TestTimerErrorIfNotRunningPublic(t *testing.T) {
	timer := NewTimer("", USER_TIME_MESSAGE)
	_, err := timer.stop()
	if err == nil {
		t.Fatal("expected error stopping timer that wasn't started")
	}
}

func TestCustomLoggerPublic(t *testing.T) {
	logger := &MyLogger{}
	timer := NewTimer("", USER_TIME_MESSAGE)
	timer._logger = logger.Log
	timer.Context(func(_ *Timer) { wasteCustomTime(500) })
	if ok, _ := regexp.MatchString(RE_USER_TIME_MESSAGE, logger.logs); !ok {
		t.Errorf("Logger did not output correct message")
	}
}

func TestTimerWithoutTextPublic(t *testing.T) {
	timer := NewTimer("", nil)
	timer._logger = nil
	timer.Context(func(_ *Timer) { wasteCustomTime(500) })
}

func TestLastStartsAsNaNPublic(t *testing.T) {
	tmr := NewTimer("", nil)
	if !math.IsNaN(tmr.Last) {
		t.Error("Last attribute should be NaN initially")
	}
}

func TestTimerSetsLastPublic(t *testing.T) {
	timer := NewTimer("", nil)
	timer._logger = nil
	timer.Context(func(_ *Timer) { time.Sleep(10 * time.Millisecond) })
	if timer.Last < 0.01 {
		t.Errorf("Timer last should be >= 0.01, got %v", timer.Last)
	}
}

// Additional public interface scenarios and cumulative/accumulated logic
// would follow same translation structure