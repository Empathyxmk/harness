package original

import "testing"

type StackStatesConstants struct {
	STATE_CREATED string
	STATE_INITED  string
}
var StackStatesVals = StackStatesConstants{STATE_CREATED: "created", STATE_INITED: "inited"}

type StackOrig struct {
	state   string
	result  interface{}
	cb      func(*StackOrig)
}

func NewStackOrig() *StackOrig {
	return &StackOrig{state: StackStatesVals.STATE_CREATED}
}
func (s *StackOrig) GetState() string {
	return s.state
}
func (s *StackOrig) SetState(st string) {
	s.state = st
}
func (s *StackOrig) SetResult(r interface{}) {
	s.result = r
}
func (s *StackOrig) GetResult() interface{} {
	return s.result
}
func (s *StackOrig) SetCallback(cb func(*StackOrig)) {
	s.cb = cb
}
func (s *StackOrig) OnResult() {
	if s.cb != nil {
		s.cb(s)
	}
}

func TestStackStatesAndResult(t *testing.T) {
	s := NewStackOrig()
	if s.GetState() != StackStatesVals.STATE_CREATED {
		t.Errorf("Initial state is %v, want %v", s.GetState(), StackStatesVals.STATE_CREATED)
	}
	s.SetState(StackStatesVals.STATE_INITED)
	if s.GetState() != StackStatesVals.STATE_INITED {
		t.Errorf("State after SetState is %v, want %v", s.GetState(), StackStatesVals.STATE_INITED)
	}
	s.SetResult("result")
	if s.GetResult() != "result" {
		t.Error("GetResult did not return 'result'")
	}
}

func TestStackCallback(t *testing.T) {
	s := NewStackOrig()
	called := false
	s.SetCallback(func(stack *StackOrig) {
		called = true
		if stack != s {
			t.Error("Callback stack is not s")
		}
	})
	s.OnResult()
	if !called {
		t.Error("Callback was not called by OnResult")
	}
}