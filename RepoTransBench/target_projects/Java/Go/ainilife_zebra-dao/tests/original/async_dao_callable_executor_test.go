package original

import (
	"errors"
	"reflect"
	"testing"
)

type DummyMapperCallable struct{}

func (d *DummyMapperCallable) Add(a, b int) int {
	return a + b
}
func (d *DummyMapperCallable) ThrowError() {
	panic(errors.New("fail"))
}

type AsyncDaoCallableExecutor struct {
	mapper     any
	methodName string
	args       []any
}

func NewAsyncDaoCallableExecutor(mapper any, methodName string, args []any) *AsyncDaoCallableExecutor {
	return &AsyncDaoCallableExecutor{mapper, methodName, args}
}

func (e *AsyncDaoCallableExecutor) Call() (any, error) {
	defer func() {
		if r := recover(); r != nil {
			res, ok := r.(error)
			if ok {
				e.args = []any{res}
			}
		}
	}()
	instVal := reflect.ValueOf(e.mapper)
	method := instVal.MethodByName(e.methodName)
	results := method.Call(sliceToValueList(e.args)...)
	if len(results) == 0 {
		return nil, nil
	}
	return results[0].Interface(), nil
}

func TestAsyncDaoCallableExecutor_CallNormal(t *testing.T) {
	map := &DummyMapperCallable{}
	exec := NewAsyncDaoCallableExecutor(map, "Add", []any{3, 4})
	res, err := exec.Call()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if res != 7 {
		t.Errorf("expected 7, got %v", res)
	}
}

func TestAsyncDaoCallableExecutor_CallThrowsException(t *testing.T) {
	map := &DummyMapperCallable{}
	exec := NewAsyncDaoCallableExecutor(map, "ThrowError", nil)
	_, err := exec.Call()
	if err == nil && len(exec.args) > 0 {
		if errVal, ok := exec.args[0].(error); ok && errVal.Error() == "fail" {
			// expected, do nothing
		} else {
			t.Errorf("unexpected panic, got %v", exec.args[0])
		}
	} else if err == nil {
		t.Fatalf("expected error from Call(), got nil")
	}
}