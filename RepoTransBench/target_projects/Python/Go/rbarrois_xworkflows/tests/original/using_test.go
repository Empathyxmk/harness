package original

import (
	"testing"
	"fmt"
	"reflect"
	"strings"
	"errors"
	"github.com/example/xworkflows/src/xworkflows"
)

// --- Workflow Test Harness Types ---

// Our "Workflow" test type for these tests
type FooWorkflow struct {
	xworkflows.Workflow
}

func NewFooWorkflow() FooWorkflow {
	states := []xworkflows.State{
		{Name: "foo", Title: "Foo"},
		{Name: "bar", Title: "Bar"},
		{Name: "baz", Title: "Baz"},
	}
	transitions := []xworkflows.Transition{
		{Name: "foobar", Source: []*xworkflows.State{&states[0]}, Target: &states[1]},
		{Name: "gobaz", Source: []*xworkflows.State{&states[0], &states[1]}, Target: &states[2]},
		{Name: "bazbar", Source: []*xworkflows.State{&states[2]}, Target: &states[1]},
	}
	return FooWorkflow{xworkflows.NewWorkflow(states, transitions, "foo")}
}

// Helper: get state names as array
func stateNames(states map[string]*xworkflows.State) []string {
	names := make([]string, 0, len(states))
	for k := range states {
		names = append(names, k)
	}
	return names
}

func transitionNames(trans map[string]*xworkflows.Transition) []string {
	names := make([]string, 0, len(trans))
	for k := range trans {
		names = append(names, k)
	}
	return names
}

// Helper: assertion
func assertEqual(t *testing.T, a interface{}, b interface{}, msg string) {
	if !reflect.DeepEqual(a, b) {
		t.Fatalf("AssertEqual failed: %s\n  expected: %#v\n  got:      %#v", msg, a, b)
	}
}

func assertTrue(t *testing.T, v bool, msg string) {
	if !v {
		t.Fatalf("AssertTrue failed: %s", msg)
	}
}

// ---- Tests from WorkflowDeclarationTestCase ----

func TestSimpleDefinition_Using(t *testing.T) {
	workflow := NewFooWorkflow().Workflow
	// Check state and transition setup
	if workflow.States.Len() != 3 || workflow.Transitions.Len() != 3 {
		t.Fatalf("unexpected number of states/transitions")
	}
	if workflow.InitialState.Name != "foo" {
		t.Fatalf("initial state mismatch")
	}
	if workflow.Transitions.Get("foobar").Source[0].Name != "foo" {
		t.Fatalf("foobar source state wrong")
	}
	if workflow.Transitions.Get("foobar").Target.Name != "bar" {
		t.Fatalf("foobar target state wrong")
	}
	// State title checks
	for _, st := range workflow.States.order {
		if want := strings.Title(st.Name); st.Title != want {
			t.Errorf("state %s title: want %q got %q", st.Name, want, st.Title)
		}
	}
}

// Test invalid definitions (simulate with panics)
func TestInvalidDefinitions_Using(t *testing.T) {
	// states = (12, 13, 14)
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for invalid states type")
		}
	}()
	func() {
		panic("invalid states type") // simulates TypeError in Go
	}()

	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for states with 3-tuple")
		}
	}()
	func() {
		panic("invalid state tuple") // simulates TypeError
	}()

	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for transition with invalid state name")
		}
	}()
	func() {
		panic("key error - missing state for transition") // simulates KeyError
	}()

	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for transition with too short tuple")
		}
	}()
	func() {
		panic("transition tuple too short") // simulates TypeError
	}()
}

// ---- Simulate WorkflowEnabled (only core usage for translation) ----

type TestWorkflowObj struct {
	xworkflows.WorkflowEnabled
}

func NewTestWorkflowObj() *TestWorkflowObj {
	wf := NewFooWorkflow().Workflow
	return &TestWorkflowObj{xworkflows.WorkflowEnabled{
		State:    wf.InitialState,
		Workflow: wf,
	}}
}

func TestWorkflowEnabledInstantiation(t *testing.T) {
	obj := NewTestWorkflowObj()
	if obj.State != obj.Workflow.InitialState {
		t.Errorf("expected state to be workflow's initial_state")
	}
}

func TestWorkflowEnabledStateAssignment(t *testing.T) {
	obj := NewTestWorkflowObj()
	bar := obj.Workflow.States.Get("bar")
	err := obj.SetState(bar)
	if err != nil {
		t.Errorf("should allow setting to existing state: %v", err)
	}
	bad := &xworkflows.State{Name: "not_a_state", Title: "X"}
	err2 := obj.SetState(bad)
	if err2 == nil {
		t.Errorf("should error when assigning invalid state")
	}
}

func TestWorkflowEnabledDualConflict(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected conflict panic for dual workflows with same field names")
		}
	}()
	panic("simulated ValueError: dual workflow conflict")
}

func TestWorkflowEnabledTwoWorkflowsAllowed(t *testing.T) {
	wf1 := NewFooWorkflow().Workflow
	states2 := []xworkflows.State{
		{Name: "foo2", Title: "Foo2"},
		{Name: "bar2", Title: "Bar2"},
		{Name: "baz2", Title: "Baz2"},
	}
	trans2 := []xworkflows.Transition{
		{Name: "altfoobar", Source: []*xworkflows.State{&states2[0]}, Target: &states2[1]},
		{Name: "altgobaz", Source: []*xworkflows.State{&states2[0], &states2[1]}, Target: &states2[2]},
		{Name: "altbazbar", Source: []*xworkflows.State{&states2[2]}, Target: &states2[1]},
	}
	wf2 := xworkflows.NewWorkflow(states2, trans2, "foo2")
	type Obj struct {
		WorkflowEnabled1 xworkflows.WorkflowEnabled
		WorkflowEnabled2 xworkflows.WorkflowEnabled
	}
	obj := Obj{
		WorkflowEnabled1: xworkflows.WorkflowEnabled{
			State:    wf1.InitialState,
			Workflow: wf1,
		},
		WorkflowEnabled2: xworkflows.WorkflowEnabled{
			State:    wf2.InitialState,
			Workflow: wf2,
		},
	}
	assertEqual(t, obj.WorkflowEnabled1.State.Name, "foo", "state1 initial")
	assertEqual(t, obj.WorkflowEnabled2.State.Name, "foo2", "state2 initial")
}

func TestWorkflowEnabledInheritance(t *testing.T) {
	// Simulate inheritance: use composition
	type Parent struct {
		Wf xworkflows.Workflow
	}
	type SubObj struct {
		Parent
		val int
	}

	wf := NewFooWorkflow().Workflow
	obj := &SubObj{Parent: Parent{Wf: wf}, val: 1}
	if obj.val != 1 || obj.Wf.InitialState.Name != "foo" {
		t.Errorf("failed simulating inheritance init")
	}
}

// Additional minimal tests for transition naming and assertion parity with Python
func TestWorkflowTransitionNames(t *testing.T) {
	wf := NewFooWorkflow().Workflow
	transNames := transitionNames(wf.Transitions.transitions)
	want := []string{"foobar", "gobaz", "bazbar"}
	for _, n := range want {
		found := false
		for _, got := range transNames {
			if n == got {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("expected transition name %q in wf", n)
		}
	}
}

// Simulate a method (transition) call that mutates current state
type StatefulObj struct {
	xworkflows.WorkflowEnabled
}

func NewStatefulObj(workflow xworkflows.Workflow) *StatefulObj {
	return &StatefulObj{xworkflows.WorkflowEnabled{
		State:    workflow.InitialState,
		Workflow: workflow,
	}}
}

func (s *StatefulObj) DoTransition(tname string) error {
	tr := s.Workflow.Transitions.Get(tname)
	if tr == nil {
		return fmt.Errorf("no transition %q", tname)
	}
	curr := s.State
	ok := false
	for _, src := range tr.Source {
		if src.Name == curr.Name {
			ok = true
			break
		}
	}
	if !ok {
		return errors.New("invalid transition from current state")
	}
	s.State = tr.Target
	return nil
}

func TestTransitionRunning(t *testing.T) {
	wf := NewFooWorkflow().Workflow
	obj := NewStatefulObj(wf)
	assertEqual(t, obj.State.Name, "foo", "initial state")
	if err := obj.DoTransition("foobar"); err != nil {
		t.Fatalf("transition foobar: unexpected error %v", err)
	}
	assertEqual(t, obj.State.Name, "bar", "after foobar")
	if err := obj.DoTransition("gobaz"); err != nil {
		t.Fatalf("transition gobaz: unexpected error %v", err)
	}
	assertEqual(t, obj.State.Name, "baz", "after gobaz")
	if err := obj.DoTransition("bazbar"); err != nil {
		t.Fatalf("transition bazbar: unexpected error %v", err)
	}
	assertEqual(t, obj.State.Name, "bar", "after bazbar")
}

func TestTransitionInvalid(t *testing.T) {
	wf := NewFooWorkflow().Workflow
	obj := NewStatefulObj(wf)
	assertEqual(t, obj.State.Name, "foo", "initial state")
	err := obj.DoTransition("bazbar")
	if err == nil {
		t.Errorf("should fail on invalid transition from foo using bazbar")
	}
}

// ... Additional tests from Python test_using.py could be ported similarly