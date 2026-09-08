package original

import (
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
)

type DummyMapperRunnable struct{}

func (d *DummyMapperRunnable) DoStuff(in string) string {
	return stringToUpper(in)
}
func (d *DummyMapperRunnable) ThrowError() {
	panic(errors.New("boom!"))
}

func stringToUpper(s string) string {
	upper := []rune(s)
	for i, ch := range upper {
		if ch >= 'a' && ch <= 'z' {
			upper[i] = ch - ('a' - 'A')
		}
	}
	return string(upper)
}

type testDaoCallback struct {
	result *atomic.Value
	err    *atomic.Value
}

func (cb *testDaoCallback) OnSuccess(v any) {
	cb.result.Store(v)
}
func (cb *testDaoCallback) OnException(e error) {
	cb.err.Store(e)
}

type AsyncDaoRunnableExecutor[T any] struct {
	mapper     any
	methodName string
	args       []any
	cb         AsyncDaoCallback[T]
}

func (a *AsyncDaoRunnableExecutor[T]) Run() {
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

func TestAsyncDaoRunnableExecutor_RunSuccess(t *testing.T) {
	mapper := &DummyMapperRunnable{}
	mname := "DoStuff"
	result := &atomic.Value{}
	errResult := &atomic.Value{}
	cb := &testDaoCallback{result, errResult}
	exec := &AsyncDaoRunnableExecutor[string]{mapper, mname, []any{"hello"}, cb}
	exec.Run()
	if v := result.Load(); v != "HELLO" {
		t.Errorf("expected 'HELLO', got %v", v)
	}
	if e := errResult.Load(); e != nil {
		t.Errorf("expected nil error, got %v", e)
	}
}

func TestAsyncDaoRunnableExecutor_RunException(t *testing.T) {
	mapper := &DummyMapperRunnable{}
	mname := "ThrowError"
	result := &atomic.Value{}
	errResult := &atomic.Value{}
	cb := &testDaoCallback{result, errResult}
	exec := &AsyncDaoRunnableExecutor[string]{mapper, mname, nil, cb}
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
		if errType.Error() != "boom!" {
			t.Errorf("expected boom!, got %v", errType.Error())
		}
	}
}