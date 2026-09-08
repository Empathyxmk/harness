package public_tests

import (
	"testing"
	"fmt"
	"math"
)

type Time struct {
	Hour   int
	Minute int
	Second float64
}

func NewTime(hour, minute int, second float64) *Time {
	return &Time{Hour: hour, Minute: minute, Second: second}
}

func (t *Time) String() string {
	return fmt.Sprintf("%02d:%02d:%04.1f\n", t.Hour, t.Minute, t.Second)
}

func AddTime(a, b *Time) *Time {
	return &Time{
		Hour:   a.Hour + b.Hour,
		Minute: a.Minute + b.Minute,
		Second: a.Second + b.Second,
	}
}

func (t *Time) Add(o *Time) *Time {
	return AddTime(t, o)
}

func (t *Time) Increment(secs float64) {
	t.Second += secs
	for t.Second >= 60.0 {
		t.Second -= 60.0
		t.Minute++
	}
	for t.Minute >= 60 {
		t.Minute -= 60
		t.Hour++
	}
}

func TestToStringAndConstructorPublic(t *testing.T) {
	tm := NewTime(3, 7, 15.5)
	if tm.String() != "03:07:15.5\n" {
		t.Errorf("Expected 03:07:15.5\\n, got %q", tm.String())
	}
}

func TestAddStaticPublic(t *testing.T) {
	t1 := NewTime(5, 10, 10.5)
	t2 := NewTime(6, 20, 50.5)
	sum := AddTime(t1, t2)
	if sum.Hour != 11 {
		t.Errorf("Expected sum.Hour == 11, got %d", sum.Hour)
	}
	if sum.Minute != 30 {
		t.Errorf("Expected sum.Minute == 30, got %d", sum.Minute)
	}
	if math.Abs(sum.Second-61.0) > 1e-8 {
		t.Errorf("Expected sum.Second == 61.0, got %.8f", sum.Second)
	}
}

func TestAddInstanceWithNoRolloverPublic(t *testing.T) {
	t1 := NewTime(2, 10, 20.0)
	t2 := NewTime(2, 40, 25.0)
	sum := t1.Add(t2)
	if sum.String() != "04:50:45.0\n" {
		t.Errorf("Expected 04:50:45.0\\n, got %q", sum.String())
	}
}

func TestIncrementSimplePublic(t *testing.T) {
	tm := NewTime(1, 2, 3.0)
	tm.Increment(10.0)
	if tm.String() != "01:02:13.0\n" {
		t.Errorf("Expected 01:02:13.0\\n, got %q", tm.String())
	}
}

func TestIncrementWithMinuteRolloverPublic(t *testing.T) {
	tm := NewTime(1, 59, 59.0)
	tm.Increment(2.5)
	if tm.String() != "02:00:01.5\n" {
		t.Errorf("Expected 02:00:01.5\\n, got %q", tm.String())
	}
}