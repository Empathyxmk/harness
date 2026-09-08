package public_tests

import (
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
	"time"
)

type DummyMapperPublic struct{}

func (d *DummyMapperPublic) Repeat(in string) string {
	return in + in
}

func (d *DummyMapperPublic) ThrowsOtherError() string {
	panic(errors.New("fail!"))
}

type AsyncDaoCallback[T any] interface {
	OnSuccess(result T)
	OnException(e error)
}

type testAsyncDaoCallbackPublic struct {
	result *atomic.Value
	error  *atomic.Value
}

func (cb *testAsyncDaoCallbackPublic) OnSuccess(val any) {
	cb.result.Store(val)
}
func (cb *testAsyncDaoCallbackPublic) OnException(e error) {
	cb.error.Store(e)
}

// Simulate async mechanisms
var (
	executorServiceCreatedPublic atomic.Bool
)

func resetExecutorPublic() {
	executorServiceCreatedPublic.Store(true)
}

func disableExecutorPublic() {
	executorServiceCreatedPublic.Store(false)
}

func AsyncMapperExecutorInitPublic(min, max, q int) {
	executorServiceCreatedPublic.Store(true)
}

func AsyncMapperExecutorSubmitCallbackPublic(mapper any, methodName string, args ...any) (any, error) {
	if !executorServiceCreatedPublic.Load() {
		return nil, &AsyncDaoExceptionPublic{Msg: "AsyncMapperExecutor has not been init yet."}
	}
	instVal := reflect.ValueOf(mapper)
	method := instVal.MethodByName(methodName)
	results := method.Call(sliceToValueList(args)...)
	if len(results) == 0 {
		return nil, nil
	}
	return results[0].Interface(), nil
}

func AsyncMapperExecutorExecuteRunnablePublic(mapper any, methodName string, args []any, callback AsyncDaoCallback[string]) {
	go func() {
		defer func() {
			if r := recover(); r != nil {
				callback.OnException(errors.New(r.(error).Error()))
			}
		}()
		instVal := reflect.ValueOf(mapper)
		method := instVal.MethodByName(methodName)
		res := method.Call(sliceToValueList(args)...)
		var val string
		if len(res) > 0 {
			val, _ = res[0].Interface().(string)
		}
		callback.OnSuccess(val)
	}()
}

func AsyncMapperExecutorSetCorePoolSizePublic(int)   {}
func AsyncMapperExecutorSetMaximumPoolSizePublic(int) {}

func TestMain(m *testing.M) {
	resetExecutorPublic()
	m.Run()
}

func TestAsyncMapperExecutorPublic_SubmitCallbackReturns(t *testing.T) {
	AsyncMapperExecutorInitPublic(2, 3, 2)
	mapper := &DummyMapperPublic{}
	res, err := AsyncMapperExecutorSubmitCallbackPublic(mapper, "Repeat", "xyz")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if res != "xyzxyz" {
		t.Errorf("expected 'xyzxyz', got %v", res)
	}
}

func TestAsyncMapperExecutorPublic_ExecuteRunnableSuccess(t *testing.T) {
	AsyncMapperExecutorInitPublic(2, 3, 2)
	mapper := &DummyMapperPublic{}
	result := &atomic.Value{}
	errorRef := &atomic.Value{}
	cb := &testAsyncDaoCallbackPublic{result, errorRef}
	AsyncMapperExecutorExecuteRunnablePublic(mapper, "Repeat", []any{"bar"}, cb)
	time.Sleep(200 * time.Millisecond)
	if got := result.Load(); got != "barbar" {
		t.Errorf("expected 'barbar', got %v", got)
	}
	if err := errorRef.Load(); err != nil {
		t.Errorf("expected nil error, got %v", err)
	}
}

func TestAsyncMapperExecutorPublic_ExecuteRunnableThrows(t *testing.T) {
	AsyncMapperExecutorInitPublic(2, 3, 2)
	mapper := &DummyMapperPublic{}
	result := &atomic.Value{}
	errorRef := &atomic.Value{}
	cb := &testAsyncDaoCallbackPublic{result, errorRef}
	AsyncMapperExecutorExecuteRunnablePublic(mapper, "ThrowsOtherError", nil, cb)
	time.Sleep(200 * time.Millisecond)
	if res := result.Load(); res != nil {
		t.Errorf("expected nil, got %v", res)
	}
	if err := errorRef.Load(); err == nil {
		t.Errorf("expected error non-nil, got nil")
	} else {
		e, ok := err.(error)
		if !ok {
			t.Errorf("errorRef does not contain error: %v", err)
		} else if e.Error() != "fail!" {
			t.Errorf("expected 'fail!', got %v", e.Error())
		}
	}
}

func TestAsyncMapperExecutorPublic_CheckNullThrows(t *testing.T) {
	AsyncMapperExecutorInitPublic(2, 3, 2)
	disableExecutorPublic()
	mapper := &DummyMapperPublic{}
	_, err := AsyncMapperExecutorSubmitCallbackPublic(mapper, "Repeat", "xyz")
	if err == nil {
		t.Fatalf("expected error for uninit executor")
	}
	daoErr, ok := err.(*AsyncDaoExceptionPublic)
	if !ok {
		t.Fatalf("expected *AsyncDaoException error, got %T: %v", err, err)
	}
	if daoErr.Msg != "AsyncMapperExecutor has not been init yet." {
		t.Errorf("expected message 'AsyncMapperExecutor has not been init yet.', got %v", daoErr.Msg)
	}
	resetExecutorPublic()
}

func TestAsyncMapperExecutorPublic_SetCorePoolSizeMethods(t *testing.T) {
	AsyncMapperExecutorSetCorePoolSizePublic(2)
	AsyncMapperExecutorSetMaximumPoolSizePublic(3)
}

// ---- Helpers

func sliceToValueList(a []any) []reflect.Value {
	vs := make([]reflect.Value, len(a))
	for i, v := range a {
		vs[i] = reflect.ValueOf(v)
	}
	return vs
}

type AsyncDaoExceptionPublic struct {
	Msg string
}

func (e *AsyncDaoExceptionPublic) Error() string {
	return e.Msg
}