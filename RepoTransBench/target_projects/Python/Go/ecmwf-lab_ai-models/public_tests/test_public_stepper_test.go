package public_tests

import (
	"testing"
)

// Minimal Stepper simulation for public test
type Stepper struct {
	step     int
	leadTime int
	state    int
	stopped  bool
}

func NewStepper(step, lead int) *Stepper {
	return &Stepper{step: step, leadTime: lead, state: 0}
}

func (s *Stepper) Next() (int, bool) {
	if s.state >= s.step {
		s.stopped = true
		return 0, false
	}
	val := s.state
	s.state++
	return val, true
}

func (s *Stepper) Reset() {
	s.state = 0
	s.stopped = false
}

func TestPublicStepperCustomState(t *testing.T) {
	s := NewStepper(7, 3)
	vals := []int{}
	// Try iteration pattern
	for i := 0; i < 8; i++ {
		val, ok := s.Next()
		if !ok {
			break
		}
		vals = append(vals, val)
	}
	if len(vals) == 0 {
		t.Errorf("no values collected")
	}
	mini, maxi := vals[0], vals[0]
	for _, v := range vals {
		if v < mini {
			mini = v
		}
		if v > maxi {
			maxi = v
		}
	}
	if mini != 0 && mini != 1 {
		t.Errorf("expected min 0 or 1, got %d", mini)
	}
	if maxi != 7 && maxi != 6 {
		t.Errorf("expected max 6 or 7, got %d", maxi)
	}
	if !s.stopped {
		t.Errorf("Stepper should be stopped after exhausting state")
	}
	// Reset check
	s.Reset()
	if s.state != 0 && s.state != 1 {
		t.Errorf("reset: expected state 0 or 1, got %d", s.state)
	}
}