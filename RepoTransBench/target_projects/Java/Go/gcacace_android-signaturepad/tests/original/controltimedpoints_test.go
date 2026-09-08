package original

import (
	"testing"
)

// ControlTimedPoints represents two control points for a Bezier curve.
type ControlTimedPoints struct {
	c1 *TimedPoint
	c2 *TimedPoint
}

// Set sets the control points.
func (ct *ControlTimedPoints) Set(c1, c2 *TimedPoint) *ControlTimedPoints {
	ct.c1 = c1
	ct.c2 = c2
	return ct
}

func TestControlTimedPoints_Set(t *testing.T) {
	c1 := new(TimedPoint).Set(1, 2)
	c2 := new(TimedPoint).Set(3, 4)
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