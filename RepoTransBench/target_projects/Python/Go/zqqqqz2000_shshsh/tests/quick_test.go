package tests

import (
	"testing"
)

type P struct{ processFunc interface{} }

type IType struct{}

var I = IType{}

func (i IType) RShift(arg interface{}) *P {
	return &P{processFunc: arg}
}

func TestRightShiftIterableIsP(t *testing.T) {
	it := []string{"abc", "def"}
	result := I.RShift(it)
	if result == nil {
		t.Error("expected result is P")
	}
}
func TestPipeRightShiftPipe(t *testing.T) {
	data := []string{"x", "y"}
	p1 := I.RShift(data)
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic")
		}
	}()
	I.RShift(p1)
}
func TestPipeRightShiftFunc(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic")
		}
	}()
	I.RShift(func(x string) string { return x })
}
func TestPipeRightShiftLambda(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic")
		}
	}()
	I.RShift(func(x string) string { return x })
}
func TestPipeRightShiftList(t *testing.T) {
	p := I.RShift([]string{"foo", "bar"})
	if p == nil {
		t.Error("expected P")
	}
}