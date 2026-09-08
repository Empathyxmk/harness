package original

import (
	"testing"
)

type testJvmField struct {
	v interface{}
}

func (f *testJvmField) Set(env Env, thiz interface{}, value interface{}) {
	f.v = value
}
func (f *testJvmField) Get(env Env, thiz interface{}) interface{} {
	return f.v
}

func TestJvmField(t *testing.T) {
	field := &testJvmField{}
	field.Set(nil, nil, "abc")
	val := field.Get(nil, nil)
	if val != "abc" {
		t.Errorf("Expected 'abc', got: %v", val)
	}
}

type testJvmMethod struct {
	called bool
}

func (m *testJvmMethod) Call(env Env, thiz interface{}, args ...interface{}) { m.called = true }
func (m *testJvmMethod) GetParameterCount() int                              { return 1 }
func (m *testJvmMethod) GetName() string                                     { return "hello" }

func TestJvmMethod(t *testing.T) {
	method := &testJvmMethod{}
	method.Call(nil, nil)
	if method.GetParameterCount() != 1 {
		t.Errorf("Expected parameter count 1, got: %d", method.GetParameterCount())
	}
	if method.GetName() != "hello" {
		t.Errorf("Expected name 'hello', got: %v", method.GetName())
	}
}