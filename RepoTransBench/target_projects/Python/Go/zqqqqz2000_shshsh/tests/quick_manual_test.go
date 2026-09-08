package tests

import (
	"testing"
)

type _Itype struct{}

func (i *_Itype) RShift(arg interface{}) *_Itype { return i }
func (i *_Itype) Or(arg interface{}) *_Itype     { return i }

type Pipe struct{}

func TestIRshiftStr(t *testing.T) {
	i := &_Itype{}
	out := i.RShift("ls")
	if out == nil {
		t.Error("should have SOME output")
	}
}

func TestIRshiftInt(t *testing.T) {
	i := &_Itype{}
	out := i.RShift(3)
	if out == nil {
		t.Error("should merge fd")
	}
}

func TestIRshiftIo(t *testing.T) {
	i := &_Itype{}
	out := i.RShift(struct{}{})
	if out == nil {
		t.Error("should support io")
	}
}

func TestIRshiftIterable(t *testing.T) {
	i := &_Itype{}
	out := i.RShift([]string{"a", "b", "c"})
	if out == nil {
		t.Error("expected non-nil for iterable")
	}
}

func TestIRshiftPipe(t *testing.T) {
	i := &_Itype{}
	p := &Pipe{}
	out := i.RShift(p)
	if out == nil {
		t.Error("expect pipe accepted")
	}
}
func TestIRshiftInvalid(t *testing.T) {
	i := &_Itype{}
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic for invalid")
		}
	}()
	type Bad struct{}
	b := Bad{}
	i.RShift(b)
}
func TestIOrOperator(t *testing.T) {
	i := &_Itype{}
	out := i.Or("echo something")
	if out == nil {
		t.Error("should or output")
	}
}