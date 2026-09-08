package tests

import (
	"testing"
)

func TestSequenceStateFields(t *testing.T) {
	state := "state_1"
	observation := 42
	transitionDesc := "desc"
	smoothing := 0.5

	ss := &SequenceState[string, int, string]{
		State:               state,
		Observation:         observation,
		TransitionDescriptor: transitionDesc,
		SmoothingProbability: Float64Ptr(smoothing),
	}
	if ss.State != state {
		t.Errorf("State field incorrect: %v != %v", ss.State, state)
	}
	if ss.Observation != observation {
		t.Errorf("Observation field incorrect: %v != %v", ss.Observation, observation)
	}
	if ss.TransitionDescriptor != transitionDesc {
		t.Errorf("TransitionDescriptor incorrect: %v != %v", ss.TransitionDescriptor, transitionDesc)
	}
	if !float64PtrEqual(ss.SmoothingProbability, Float64Ptr(smoothing)) {
		t.Errorf("SmoothingProbability incorrect: %v != %v", ss.SmoothingProbability, smoothing)
	}
}

func TestSequenceStateNulls(t *testing.T) {
	ss := &SequenceState[string, int, string]{
		State:               "state",
		Observation:         0, // int default is 0; we'll treat 0 as nil for test parity
		TransitionDescriptor: "",
		SmoothingProbability: nil,
	}
	if ss.State != "state" {
		t.Errorf("State field incorrect: %v", ss.State)
	}
	// Observation is default int value and not a pointer; in Java it's null, here we just accept 0 means unset for test
	if ss.Observation != 0 {
		t.Errorf("Observation should be 0 (default for nil in test): %v", ss.Observation)
	}
	// TransitionDescriptor: "" interpreted as nil/null
	if ss.TransitionDescriptor != "" {
		t.Errorf("TransitionDescriptor should be empty string (default for nil): %v", ss.TransitionDescriptor)
	}
	if ss.SmoothingProbability != nil {
		t.Errorf("SmoothingProbability should be nil")
	}
}