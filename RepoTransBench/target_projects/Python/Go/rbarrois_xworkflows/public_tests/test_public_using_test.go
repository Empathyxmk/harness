package public_tests

import (
	"testing"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestPublicWorkflowEnabledInvalidSettingAndImplementationConflict(t *testing.T) {
	states := []xworkflows.State{{Name: "begin", Title: "Begin"}, {Name: "end", Title: "End"}}
	transitions := []xworkflows.Transition{{Name: "begin_to_end", Source: []*xworkflows.State{&states[0]}, Target: &states[1]}}
	wf := xworkflows.NewWorkflow(states, transitions, "begin")
	obj := &xworkflows.WorkflowEnabled{Workflow: wf, State: wf.States.Get("begin")}
	// setting to a completely arbitrary state yields error
	if err := obj.SetState(&xworkflows.State{Name: "unknown_state", Title: "No State"}); err == nil {
		t.Errorf("expected error when assigning arbitrary State")
	}
	// assigning an int to a workflow-enabled attribute (simulate)
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic when assigning non-State")
		}
	}()
	var bogus interface{} = 98765
	_ = bogus.(xworkflows.State)
}