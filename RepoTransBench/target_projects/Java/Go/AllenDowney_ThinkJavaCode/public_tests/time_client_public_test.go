package public_tests

import (
	"testing"
	"math"
	"fmt"
)

type Time2 struct {
	Hour   int
	Minute int
	Second float64
}

func NewTime2(hour, minute int, second float64) *Time2 {
	return &Time2{Hour: hour, Minute: minute, Second: second}
}

func (t *Time2) String() string {
	return fmt.Sprintf("%02d:%02d:%04.1f\n", t.Hour, t.Minute, t.Second)
}

func AddTime2(a, b *Time2) *Time2 {
	return &Time2{
		Hour:   a.Hour + b.Hour,
		Minute: a.Minute + b.Minute,
		Second: a.Second + b.Second,
	}
}

func (t *Time2) Add(o *Time2) *Time2 {
	return AddTime2(t, o)
}

func (t *Time2) Increment(secs float64) {
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

func TestCustomToStringPublic(t *testing.T) {
	tm := NewTime2(2, 45, 30.0)
	if tm.String() != "02:45:30.0\n" {
		t.Errorf("Expected 02:45:30.0\\n, got %q", tm.String())
	}
}

func TestAddAndIncrementWithDiffDataPublic(t *testing.T) {
	t1 := NewTime2(3, 15, 25.0)
	t2 := NewTime2(4, 25, 35.0)
	sum := AddTime2(t1, t2)
	if sum.Hour != 7 {
		t.Errorf("Expected sum.Hour == 7, got %d", sum.Hour)
	}
	if sum.Minute != 40 {
		t.Errorf("Expected sum.Minute == 40, got %d", sum.Minute)
	}
	if math.Abs(sum.Second-60.0) > 1e-8 {
		t.Errorf("Expected sum.Second == 60.0, got %.8f", sum.Second)
	}

	t1.Increment(36.5)
	if t1.String() != "03:16:01.5\n" {
		t.Errorf("Expected 03:16:01.5\\n, got %q", t1.String())
	}
}