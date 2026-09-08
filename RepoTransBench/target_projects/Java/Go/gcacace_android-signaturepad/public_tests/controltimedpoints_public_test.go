package public_tests

import (
	"testing"
)

type ControlTimedPoints struct {
	c1 *TimedPoint
	c2 *TimedPoint
}

func (ct *ControlTimedPoints) Set(c1, c2 *TimedPoint) *ControlTimedPoints {
	ct.c1 = c1
	ct.c2 = c2
	return ct
}

func TestControlTimedPoints_SetWithDifferentPoints(t *testing.T) {
	c1 := new(TimedPoint).Set(-5.5, 42.42)
	c2 := new(TimedPoint).Set(100, -200)
	control := &ControlTimedPoints{}
	if control.Set(c1, c2) != control {
		t.Errorf("Expected Set to return receiver")
	}
	if control.c1 != c1 {
		t.Errorf("Expected c1=%v, got %v", c1, control.c1)
	}
	if control.c2 != c2 {
		t.Errorf("Expected c2=%v, got %v", c2, control.c2)
	}
}