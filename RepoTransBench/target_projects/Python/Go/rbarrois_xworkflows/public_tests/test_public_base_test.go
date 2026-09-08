package public_tests

import (
	"testing"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestPublicWorkflowStatesAndTransitions(t *testing.T) {
	states := []xworkflows.State{{Name: "start", Title: "Start"},
		{Name: "mid", Title: "Middle"}, {Name: "end", Title: "End"}}
	transitions := []xworkflows.Transition{
		{Name: "go_mid", Source: []*xworkflows.State{&states[0]}, Target: &states[1]},
		{Name: "finish", Source: []*xworkflows.State{&states[1]}, Target: &states[2]},
		{Name: "reset", Source: []*xworkflows.State{&states[2]}, Target: &states[0]},
	}
	wf := xworkflows.NewWorkflow(states, transitions, "start")
	if wf.States.Len() != 3 {
		t.Errorf("expected 3 states")
	}
	if wf.States.Get("start").Title != "Start" {
		t.Errorf("wrong title for start")
	}
	if wf.Transitions.Get("go_mid").Source[0].Name != "start" {
		t.Errorf("wrong source for go_mid")
	}
	if wf.Transitions.Get("finish").Target.Name != "end" {
		t.Errorf("wrong target for finish")
	}
	if wf.InitialState != wf.States.Get("start") {
		t.Errorf("initial state should be 'start'")
	}
}

func TestPublicWorkflowInvalidStateTransition(t *testing.T) {
	states := []xworkflows.State{{Name: "a", Title: "Alpha"}, {Name: "b", Title: "Beta"}}
	transitions := []xworkflows.Transition{{Name: "a_to_b", Source: []*xworkflows.State{&states[0]}, Target: &states[1]}}
	_ = xworkflows.NewWorkflow(states, transitions, "a")
	badTransition := func() {
		badStates := []xworkflows.State{{Name: "x", Title: "Ex"}, {Name: "y", Title: "Why"}}
		badTransitions := []xworkflows.Transition{{Name: "invalid", Source: []*xworkflows.State{&badStates[0]}, Target: nil}}
		_ = xworkflows.NewWorkflow(badStates, badTransitions, "x")
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for referencing an invalid state")
		}
	}()
	badTransition()
}