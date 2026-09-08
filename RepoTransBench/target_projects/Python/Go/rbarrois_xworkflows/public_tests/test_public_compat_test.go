package public_tests

import (
	"testing"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestPublicStringTypeIsStr(t *testing.T) {
	name := reflect.TypeOf(xworkflows.Workflow{}).Name()
	if name == "" {
		t.Errorf("expected a name for Workflow struct type")
	}
}

func TestPublicBaseWorkflowHasStates(t *testing.T) {
	states := []xworkflows.State{{Name: "alpha", Title: "Alpha"}, {Name: "beta", Title: "Beta"}}
	transitions := []xworkflows.Transition{{Name: "ab", Source: []*xworkflows.State{&states[0]}, Target: &states[1]}}
	workflow := xworkflows.NewWorkflow(states, transitions, "alpha")
	if workflow.States.Get("alpha") == nil {
		t.Errorf("'alpha' not found in workflow states")
	}
	if workflow.States.Get("beta").Title != "Beta" {
		t.Errorf("beta state title mismatch")
	}
}