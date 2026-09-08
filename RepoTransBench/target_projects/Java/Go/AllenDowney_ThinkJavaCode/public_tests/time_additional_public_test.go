package public_tests

import (
	"testing"
	"math"
)

type Time3 struct {
	Hour   int
	Minute int
	Second float64
}

func NewTime3(hour, minute int, second float64) *Time3 {
	return &Time3{Hour: hour, Minute: minute, Second: second}
}

func timeToSeconds(t *Time3) float64 {
	return float64(t.Hour)*3600 + float64(t.Minute)*60 + t.Second
}
func secondsToTime(seconds float64) *Time3 {
	h := int(seconds / 3600)
	seconds -= float64(h) * 3600
	m := int(seconds / 60)
	seconds -= float64(m) * 60
	return &Time3{Hour: h, Minute: m, Second: seconds}
}
func subtractTime(t1, t2 *Time3) *Time3 {
	secT1 := timeToSeconds(t1)
	secT2 := timeToSeconds(t2)
	diff := secT1 - secT2
	return secondsToTime(diff)
}

func TestTimeToSecondsAndConversion(t *testing.T) {
	tm := NewTime3(6, 4, 15.0)
	seconds := timeToSeconds(tm)
	expected := 6*3600 + 4*60 + 15.0
	if math.Abs(seconds-expected) > 1e-8 {
		t.Errorf("Expected %v, got %v", expected, seconds)
	}
	t2 := secondsToTime(3678.5)
	if t2.Hour != 1 {
		t.Errorf("Expected hour==1, got %d", t2.Hour)
	}
	if t2.Minute != 1 {
		t.Errorf("Expected minute==1, got %d", t2.Minute)
	}
	if math.Abs(t2.Second-18.5) > 1e-8 {
		t.Errorf("Expected 18.5, got %v", t2.Second)
	}
}

func TestSubtractTime(t *testing.T) {
	t1 := NewTime3(7, 10, 15.0)
	t2 := NewTime3(4, 20, 15.0)
	diff := subtractTime(t1, t2)
	if diff.Hour != 2 {
		t.Errorf("Expected hour==2, got %d", diff.Hour)
	}
	if diff.Minute != 50 {
		t.Errorf("Expected minute==50, got %d", diff.Minute)
	}
	if math.Abs(diff.Second) > 1e-8 {
		t.Errorf("Expected second==0.0, got %v", diff.Second)
	}
}