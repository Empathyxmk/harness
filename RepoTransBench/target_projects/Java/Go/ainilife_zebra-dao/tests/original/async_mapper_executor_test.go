package original

import (
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
	"time"
)

type DummyMapper struct{}

func (d *DummyMapper) Reverse(in string) string {
	runes := []rune(in)
	l, r := 0, len(runes)-1
	for l < r {
		runes[l], runes[r] = runes[r], runes[l]
		l++
		r--
	}
	return string(runes)
}

func (d *DummyMapper) ThrowsError() string {
	panic(errors.New("err!"))
}

type AsyncDaoCallback[T any] interface {
	OnSuccess(result T)
	OnException(e error)
}

type testAsyncDaoCallback struct {
	result *atomic.Value
	error  *atomic.Value
}

func (cb *testAsyncDaoCallback) OnSuccess(val any) {
	cb.result.Store(val)
}
func (cb *testAsyncDaoCallback) OnException(e error) {
	cb.error.Store(e)
}

// --- Simulate async mechanisms ---

// global executor variables
var (
	executorServiceCreated atomic.Bool
	testAsyncResult any
	testAsyncErr error
)

func resetExecutor() {
	executorServiceCreated.Store(true)
}

func disableExecutor() {
	executorServiceCreated.Store(false)
}

func AsyncMapperExecutorInit(min, max, q int) {
	// Simulate pool init
	executorServiceCreated.Store(true)
}

func AsyncMapperExecutorSubmitCallback(mapper any, methodName string, args ...any) (any, error) {
	if !executorServiceCreated.Load() {
		return nil, &AsyncDaoException{Msg: "AsyncMapperExecutor has not been init yet."}
	}
	instVal := reflect.ValueOf(mapper)
	method := instVal.MethodByName(methodName)
	results := method.Call(sliceToValueList(args)...)
	if len(results) == 0 {
		return nil, nil
	}
	// For test, support either panic, or return result
	if results[len(results)-1].Kind() == reflect.Interface || results[len(results)-1].Kind() == reflect.Ptr {
		last := results[len(results)-1].Interface()
		if last != nil {
			if err, ok := last.(error); ok && err != nil {
				return nil, err
			}
		}
	}
	return results[0].Interface(), nil
}

func AsyncMapperExecutorExecuteRunnable(mapper any, methodName string, args []any, callback AsyncDaoCallback[string]) {
	go func() {
		defer func() {
			if r := recover(); r != nil {
				callback.OnException(errors.New(r.(error).Error()))
			}
		}()
		instVal := reflect.ValueOf(mapper)
		method := instVal.MethodByName(methodName)
		res := method.Call(sliceToValueList(args)...)
		// Support simple result only
		var val string
		if len(res) > 0 {
			val, _ = res[0].Interface().(string)
		}
		callback.OnSuccess(val)
	}()
}

func AsyncMapperExecutorSetCorePoolSize(int)   {}
func AsyncMapperExecutorSetMaximumPoolSize(int) {}

func TestMain(m *testing.M) {
	// Make sure each run starts executor
	resetExecutor()
	m.Run()
}

func TestAsyncMapperExecutor_SubmitCallbackReturns(t *testing.T) {
	AsyncMapperExecutorInit(1, 2, 2)
	mapper := &DummyMapper{}
	res, err := AsyncMapperExecutorSubmitCallback(mapper, "Reverse", "abc")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if res != "cba" {
		t.Errorf("expected 'cba', got %v", res)
	}
}

func TestAsyncMapperExecutor_ExecuteRunnableSuccess(t *testing.T) {
	AsyncMapperExecutorInit(1, 2, 2)
	mapper := &DummyMapper{}
	result := &atomic.Value{}
	errorRef := &atomic.Value{}
	cb := &testAsyncDaoCallback{result, errorRef}
	AsyncMapperExecutorExecuteRunnable(mapper, "Reverse", []any{"foo"}, cb)
	time.Sleep(200 * time.Millisecond)
	if got := result.Load(); got != "oof" {
		t.Errorf("expected 'oof', got %v", got)
	}
	if err := errorRef.Load(); err != nil {
		t.Errorf("expected nil error, got %v", err)
	}
}

func TestAsyncMapperExecutor_ExecuteRunnableThrows(t *testing.T) {
	AsyncMapperExecutorInit(1, 2, 2)
	mapper := &DummyMapper{}
	result := &atomic.Value{}
	errorRef := &atomic.Value{}
	cb := &testAsyncDaoCallback{result, errorRef}
	AsyncMapperExecutorExecuteRunnable(mapper, "ThrowsError", nil, cb)
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
		} else if e.Error() != "err!" {
			t.Errorf("expected 'err!', got %v", e.Error())
		}
	}
}

func TestAsyncMapperExecutor_CheckNullThrows(t *testing.T) {
	AsyncMapperExecutorInit(1,2,2)
	disableExecutor()
	mapper := &DummyMapper{}
	_, err := AsyncMapperExecutorSubmitCallback(mapper, "Reverse", "abc")
	if err == nil {
		t.Fatalf("expected error for uninit executor")
	}
	daoErr, ok := err.(*AsyncDaoException)
	if !ok {
		t.Fatalf("expected *AsyncDaoException error, got %T: %v", err, err)
	}
	if daoErr.Msg != "AsyncMapperExecutor has not been init yet." {
		t.Errorf("expected specific error message, got %v", daoErr.Msg)
	}
	// restore
	resetExecutor()
}

func TestAsyncMapperExecutor_SetCorePoolSizeMethods(t *testing.T) {
	AsyncMapperExecutorSetCorePoolSize(1)
	AsyncMapperExecutorSetMaximumPoolSize(2)
	// No assertion, just coverage.
}

// --- Helpers ---

func sliceToValueList(a []any) []reflect.Value {
	vs := make([]reflect.Value, len(a))
	for i, v := range a {
		vs[i] = reflect.ValueOf(v)
	}
	return vs
}

type AsyncDaoException struct {
	Msg string
}

func (e *AsyncDaoException) Error() string {
	return e.Msg
}