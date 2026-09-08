package tests

import (
	"bytes"
	"log"
	"strings"
	"testing"
)

// Dummy Stepper for test logic
type Stepper struct {
	step     int
	leadTime int
	numSteps int
	logBuf   *bytes.Buffer
	logger   *log.Logger
}

func NewStepper(step, leadTime int, logger *log.Logger) *Stepper {
	steps := 0
	if step > 0 {
		steps = (leadTime + step - 1) / step
	}
	return &Stepper{
		step:     step,
		leadTime: leadTime,
		numSteps: steps,
		logger:   logger,
	}
}

func (s *Stepper) Start() {
	if s.logger != nil {
		s.logger.Printf("Started stepper")
	}
}

func (s *Stepper) Stop() {
	if s.logger != nil {
		s.logger.Printf("Elapsed: ...\nAverage: ...")
	}
}

// Call is single step.
func (s *Stepper) Call(i, n int) {
	if s.logger != nil {
		s.logger.Printf("Step %d/%d\n", i+1, n)
	}
}

func TestStepperBasic(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "", 0)
	s := NewStepper(2, 6, logger)
	if s.numSteps != 3 {
		t.Errorf("expected numSteps=3, got %d", s.numSteps)
	}
	s.Start()
	s.Call(0, 2)
	s.Call(1, 2)
	s.Call(2, 2)
	s.Stop()
	logs := buf.String()
	if !strings.Contains(logs, "Elapsed") {
		t.Errorf("expected 'Elapsed' in logs:\n%s", logs)
	}
	if !strings.Contains(logs, "Average") {
		t.Errorf("expected 'Average' in logs:\n%s", logs)
	}
}

func TestStepperZeroSteps(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "", 0)
	s := NewStepper(5, 0, logger)
	s.Start()
	s.Stop()
	logs := buf.String()
	if strings.Contains(logs, "Average") {
		t.Errorf("should not log Average per step if zero lead_time")
	}
}