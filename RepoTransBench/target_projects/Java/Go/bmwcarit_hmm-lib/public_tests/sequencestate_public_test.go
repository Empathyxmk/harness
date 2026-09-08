package public_tests

import (
	"bmwcarit_hmm_lib/tests"
	"testing"
)

func TestSequenceStateFieldsPublic(t *testing.T) {
	state := "state_2"
	observation := 99
	transitionDesc := "public_desc"
	smoothing := 0.75

	ss := &tests.SequenceState[string, int, string]{
		State:               state,
		Observation:         observation,
		TransitionDescriptor: transitionDesc,
		SmoothingProbability: tests.Float64Ptr(smoothing),
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
	if !tests.Float64PtrEqual(ss.SmoothingProbability, tests.Float64Ptr(smoothing)) {
		t.Errorf("SmoothingProbability incorrect: %v != %v", ss.SmoothingProbability, smoothing)
	}
}

func TestSequenceStateNullsPublic(t *testing.T) {
	ss := &tests.SequenceState[string, int, string]{
		State:               "public_state",
		Observation:         0,
		TransitionDescriptor: "",
		SmoothingProbability: nil,
	}
	if ss.State != "public_state" {
		t.Errorf("State field incorrect: %v", ss.State)
	}
	// Observation is default int value and not a pointer; in Java it's null, here we accept 0 as unset for parity
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