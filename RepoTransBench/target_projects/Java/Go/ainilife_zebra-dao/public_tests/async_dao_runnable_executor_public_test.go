package public_tests

import (
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
)

type DummyMapperRunnablePublic struct{}

func (d *DummyMapperRunnablePublic) DoOtherStuff(input string) string {
	runes := []rune(input)
	l, r := 0, len(runes)-1
	for l < r {
		runes[l], runes[r] = runes[r], runes[l]
		l++
		r--
	}
	return string(runes)
}
func (d *DummyMapperRunnablePublic) ThrowOtherError() {
	panic(errors.New("boom2!"))
}

type testDaoCallbackPublic struct {
	result *atomic.Value
	err    *atomic.Value
}

func (cb *testDaoCallbackPublic) OnSuccess(v any) {
	cb.result.Store(v)
}
func (cb *testDaoCallbackPublic) OnException(e error) {
	cb.err.Store(e)
}

type AsyncDaoRunnableExecutorPublic[T any] struct {
	mapper     any
	methodName string
	args       []any
	cb         AsyncDaoCallback[T]
}

func (a *AsyncDaoRunnableExecutorPublic[T]) Run() {
	defer func() {
		if r := recover(); r != nil {
			a.cb.OnException(r.(error))
		}
	}()
	instVal := reflect.ValueOf(a.mapper)
	method := instVal.MethodByName(a.methodName)
	results := method.Call(sliceToValueList(a.args)...)
	var val T
	if len(results) > 0 {
		valAny := results[0].Interface()
		val, _ = valAny.(T)
	}
	a.cb.OnSuccess(val)
}

func TestAsyncDaoRunnableExecutorPublic_RunSuccess(t *testing.T) {
	mapper := &DummyMapperRunnablePublic{}
	mname := "DoOtherStuff"
	result := &atomic.Value{}
	errResult := &atomic.Value{}
	cb := &testDaoCallbackPublic{result, errResult}
	exec := &AsyncDaoRunnableExecutorPublic[string]{mapper, mname, []any{"world"}, cb}
	exec.Run()
	if v := result.Load(); v != "dlrow" {
		t.Errorf("expected 'dlrow', got %v", v)
	}
	if e := errResult.Load(); e != nil {
		t.Errorf("expected nil error, got %v", e)
	}
}

func TestAsyncDaoRunnableExecutorPublic_RunException(t *testing.T) {
	mapper := &DummyMapperRunnablePublic{}
	mname := "ThrowOtherError"
	result := &atomic.Value{}
	errResult := &atomic.Value{}
	cb := &testDaoCallbackPublic{result, errResult}
	exec := &AsyncDaoRunnableExecutorPublic[string]{mapper, mname, nil, cb}
	exec.Run()
	if v := result.Load(); v != nil {
		t.Errorf("expected nil, got %v", v)
	}
	if e := errResult.Load(); e == nil {
		t.Fatal("expected non-nil error")
	} else {
		errType, ok := e.(error)
		if !ok {
			t.Fatalf("errResult not error type: %v", e)
		}
		if errType.Error() != "boom2!" {
			t.Errorf("expected boom2!, got %v", errType.Error())
		}
	}
}