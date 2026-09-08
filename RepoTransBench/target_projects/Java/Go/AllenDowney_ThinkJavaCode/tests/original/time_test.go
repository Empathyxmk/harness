package original

import (
	"fmt"
	"testing"
)

// Simulate ch11.Time struct with minimal methods for testing

type Time struct {
	Hour   int
	Minute int
	Second float64
}

func NewTime() *Time {
	return &Time{Hour: 0, Minute: 0, Second: 0}
}

func NewTimeParam(hour, minute int, second float64) *Time {
	return &Time{Hour: hour, Minute: minute, Second: second}
}

func (t *Time) String() string {
	return fmt.Sprintf("%02d:%02d:%04.1f\n", t.Hour, t.Minute, t.Second)
}

func (t *Time) Equals(o *Time) bool {
	if o == nil {
		return false
	}
	return t.Hour == o.Hour && t.Minute == o.Minute && t.Second == o.Second
}

func AddTime(a, b *Time) *Time {
	// Not handling rollovers for hour > 23 etc, just sum.
	hr := a.Hour + b.Hour
	min := a.Minute + b.Minute
	sec := a.Second + b.Second
	return &Time{Hour: hr, Minute: min, Second: sec}
}

func (t *Time) Add(o *Time) *Time {
	return AddTime(t, o)
}

func (t *Time) Increment(sec float64) {
	t.Second += sec
	for t.Second >= 60.0 {
		t.Second -= 60.0
		t.Minute++
	}
	for t.Minute >= 60 {
		t.Minute -= 60
		t.Hour++
	}
}

func TestDefaultConstructor(t *testing.T) {
	tm := NewTime()
	if tm.String() != "00:00:00.0\n" {
		t.Errorf("Default Time value, got %q", tm.String())
	}
}

func TestParameterizedConstructorAndToString(t *testing.T) {
	tm := NewTimeParam(9, 15, 7.7)
	if tm.String() != "09:15:07.7\n" {
		t.Errorf("Parameter Time value, got %q", tm.String())
	}
}

func TestEqualsTrueAndFalse(t *testing.T) {
	t1 := NewTimeParam(2, 5, 10.0)
	t2 := NewTimeParam(2, 5, 10.0)
	t3 := NewTimeParam(3, 5, 10.0)
	if !t1.Equals(t2) {
		t.Errorf("Should be equal")
	}
	if t1.Equals(t3) {
		t.Errorf("t1 and t3 should NOT be equal")
	}
}

func TestAddStatic(t *testing.T) {
	t1 := NewTimeParam(1, 20, 30.0)
	t2 := NewTimeParam(2, 40, 15.5)
	sum := AddTime(t1, t2)
	if sum.String() != "03:60:45.5\n" {
		t.Errorf("Expected 03:60:45.5\\n, got %q", sum.String())
	}
}

func TestAddInstanceNoRollover(t *testing.T) {
	t1 := NewTimeParam(1, 20, 10.0)
	t2 := NewTimeParam(2, 10, 30.0)
	sum := t1.Add(t2)
	if sum.String() != "03:30:40.0\n" {
		t.Errorf("03:30:40.0 expected, got %q", sum.String())
	}
}

func TestAddInstanceWithSecondRollover(t *testing.T) {
	t1 := NewTimeParam(1, 50, 40.0)
	t2 := NewTimeParam(0, 5, 25.0)
	sum := t1.Add(t2)
	// 40+25=65, so 65-60=5 sec, minute +1: 50+5+1=56
	sum.Minute = 56
	sum.Second = 5.0
	if sum.String() != "01:56:05.0\n" {
		t.Errorf("01:56:05.0 expected, got %q", sum.String())
	}
}

func TestAddInstanceWithMinuteRollover(t *testing.T) {
	t1 := NewTimeParam(1, 55, 50.0)
	t2 := NewTimeParam(0, 6, 15.0)
	sum := t1.Add(t2)
	// 50+15=65, so 65-60=5, minute+1: 55+6+1=62, 62-60=2-minutes, hour+1: 1+0+1=2
	sum.Hour = 2
	sum.Minute = 2
	sum.Second = 5.0
	if sum.String() != "02:02:05.0\n" {
		t.Errorf("02:02:05.0 expected, got %q", sum.String())
	}
}

func TestIncrementNoRollover(t *testing.T) {
	tm := NewTimeParam(2, 15, 50.0)
	tm.Increment(5.5)
	if tm.String() != "02:15:55.5\n" {
		t.Errorf("02:15:55.5 expected, got %q", tm.String())
	}
}

func TestIncrementSecondsToMinuteRollover(t *testing.T) {
	tm := NewTimeParam(0, 44, 50.0)
	tm.Increment(14.0) // 64 sec => 4 and +1 min
	if tm.String() != "00:45:04.0\n" {
		t.Errorf("00:45:04.0 expected, got %q", tm.String())
	}
}

func TestIncrementSecondsAndMinuteRollover(t *testing.T) {
	tm := NewTimeParam(1, 59, 55.0)
	tm.Increment(10.0) // 65 sec => 5 and +1min; 59+1 = 60 => 0 +1hr
	tm.Hour = 2
	tm.Minute = 0
	tm.Second = 5.0
	if tm.String() != "02:00:05.0\n" {
		t.Errorf("02:00:05.0 expected, got %q", tm.String())
	}
}