package public_tests

import (
	"testing"
)

type PublicMock struct {
	helloFn      func() string
	called       bool
	returnValue  int
	callCount    int
	callArgs     []interface{}
	callArgsList [][]interface{}
}

func (m *PublicMock) Hello() string {
	if m.helloFn != nil {
		return m.helloFn()
	}
	return ""
}
func (m *PublicMock) Call(args ...interface{}) int {
	m.called = true
	m.callCount++
	m.callArgs = args
	m.callArgsList = append(m.callArgsList, args)
	return m.returnValue
}
func (m *PublicMock) ResetMock() {
	m.called = false
	m.callCount = 0
	m.callArgs = nil
	m.callArgsList = nil
}

func TestPublicBasicMock(t *testing.T) {
	m := &PublicMock{}
	m.helloFn = func() string { return "moon" }
	if m.Hello() != "moon" {
		t.Error("Expected hello to return 'moon'")
	}
}

func TestPublicSideEffect(t *testing.T) {
	val := []string{}
	m := &PublicMock{}
	m.helloFn = func() string {
		val = append(val, "invoked")
		return ""
	}
	m.Hello()
	found := false
	for _, v := range val {
		if v == "invoked" {
			found = true
		}
	}
	if !found {
		t.Error("Side effect not triggered.")
	}
}

func TestPublicCallArgs(t *testing.T) {
	m := &PublicMock{}
	m.Call("b", "y")
	if m.callArgs[0] != "b" {
		t.Error("call args mismatch")
	}
}

func TestPublicMockReturnValue(t *testing.T) {
	m := &PublicMock{returnValue: 55}
	if m.Call() != 55 {
		t.Error("Expected return value 55")
	}
	m.returnValue = 23
	if m.Call() != 23 {
		t.Error("Expected return value 23")
	}
}

func TestPublicMockReset(t *testing.T) {
	m := &PublicMock{}
	m.Call("b")
	if !m.called {
		t.Error("expected called == true after call")
	}
	m.ResetMock()
	if m.called {
		t.Error("expected called == false after reset")
	}
}