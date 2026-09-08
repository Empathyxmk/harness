package public_tests

import (
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
)

type DummyCallable struct{}

func (d *DummyCallable) Calc(a, b int) int {
	return a - b
}

func (d *DummyCallable) ThrowSomething() int {
	panic(errors.New("sub_fail"))
}

type testCallbackCallable struct {
	output *atomic.Value
	err    *atomic.Value
	fired  *atomic.Bool
}

func (cb *testCallbackCallable) OnSuccess(val any) {
	cb.output.Store(val)
}
func (cb *testCallbackCallable) OnException(e error) {
	cb.err.Store(e)
	cb.fired.Store(true)
}

type AsyncDaoCallableExecutorPublic[T any] struct {
	mapper     any
	methodName string
	args       []any
	cb         AsyncDaoCallback[T]
}

func NewAsyncDaoCallableExecutorPublic(mapper any, methodName string, args []any, cb AsyncDaoCallback[any]) *AsyncDaoCallableExecutorPublic[any] {
	return &AsyncDaoCallableExecutorPublic[any]{mapper, methodName, args, cb}
}

func (e *AsyncDaoCallableExecutorPublic[T]) Call() (any, error) {
	defer func() {
		if r := recover(); r != nil {
			if e.cb != nil {
				e.cb.OnException(r.(error))
			}
		}
	}()
	instVal := reflect.ValueOf(e.mapper)
	method := instVal.MethodByName(e.methodName)
	results := method.Call(sliceToValueList(e.args)...)
	if len(results) == 0 {
		return nil, nil
	}
	if e.cb != nil {
		e.cb.OnSuccess(results[0].Interface())
	}
	return results[0].Interface(), nil
}

func TestAsyncDaoCallableExecutorPublic_CallableRunSuccess(t *testing.T) {
	inst := &DummyCallable{}
	output := &atomic.Value{}
	errV := &atomic.Value{}
	cb := &testCallbackCallable{output, errV, &atomic.Bool{}}
	exec := &AsyncDaoCallableExecutorPublic[int]{mapper: inst, methodName: "Calc", args: []any{8, 3}, cb: cb}
	val, err := exec.Call()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if val != 5 {
		t.Errorf("expected 5, got %v", val)
	}
	if errV.Load() != nil {
		t.Errorf("expected no error, got %v", errV.Load())
	}
	if output.Load() != 5 {
		t.Errorf("expected output 5, got %v", output.Load())
	}
}

func TestAsyncDaoCallableExecutorPublic_CallableThrowsException(t *testing.T) {
	inst := &DummyCallable{}
	output := &atomic.Value{}
	errV := &atomic.Value{}
	fired := &atomic.Bool{}
	cb := &testCallbackCallable{output, errV, fired}
	exec := &AsyncDaoCallableExecutorPublic[int]{mapper: inst, methodName: "ThrowSomething", cb: cb}
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic, got none")
		}
	}()
	_, _ = exec.Call()
	if output.Load() != nil {
		t.Errorf("expected output nil, got %v", output.Load())
	}
	if !fired.Load() {
		t.Errorf("expected exception fired")
	}
	if errV.Load() == nil {
		t.Errorf("expected error, got nil")
	} else {
		if e, ok := errV.Load().(error); ok {
			if e.Error() != "sub_fail" {
				t.Errorf("expected 'sub_fail', got %v", e.Error())
			}
		} else {
			t.Errorf("error is not proper error, got %v", errV.Load())
		}
	}
}

// helpers
func sliceToValueList(a []any) []reflect.Value {
	vs := make([]reflect.Value, len(a))
	for i, v := range a {
		vs[i] = reflect.ValueOf(v)
	}
	return vs
}