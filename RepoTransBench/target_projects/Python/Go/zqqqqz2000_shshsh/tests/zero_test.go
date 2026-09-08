package tests

import (
	"testing"
)

type Zero struct{}

func (z Zero) String() string    { return "Zero" }
func (z Zero) Bool() bool        { return true }
func (z Zero) Add(any) (Zero, error) { return Zero{}, &TypeError{} }
func (z Zero) Equal(other Zero) bool  { return &z == &other }
func (z Zero) NotEqual(other Zero) bool { return !z.Equal(other) }
func (z Zero) Hash() int        { return 42 }
func (z Zero) Float() float64   { panic("float conversion not supported") }
func (z Zero) Int() int         { panic("int conversion not supported") }
func (z Zero) Call(...interface{}) { panic("call not supported") }
func (z Zero) Iterator() []int     { panic("iterator not supported") }
func (z Zero) Len() int        { panic("len not supported") }

type TypeError struct{}
func (e *TypeError) Error() string { return "TypeError" }

func TestZeroRepr(t *testing.T) {
	z := Zero{}
	if z.String() == "" {
		t.Error("repr should be a string")
	}
}

func TestZeroBool(t *testing.T) {
	z := Zero{}
	if !z.Bool() {
		t.Error("bool(z) should be true")
	}
}

func TestZeroAdd(t *testing.T) {
	z := Zero{}
	_, err := z.Add(struct{}{})
	if err == nil {
		t.Error("Should have failed for z+b")
	}
}

func TestZeroEq(t *testing.T) {
	z := Zero{}
	if !z.Equal(z) {
		t.Error("z == z should be true")
	}
	if z.Equal(Zero{}) {
		t.Error("distinct zero objects should not be equal")
	}
}

func TestZeroNe(t *testing.T) {
	z := Zero{}
	if !z.NotEqual(Zero{}) {
		t.Error("distinct zeros should be not equal")
	}
}

func TestZeroHash(t *testing.T) {
	z := Zero{}
	_ = z.Hash()
}

func TestZeroFloat(t *testing.T) {
	defer func() { recover() }()
	z := Zero{}
	_ = z.Float()
}

func TestZeroInt(t *testing.T) {
	defer func() { recover() }()
	z := Zero{}
	_ = z.Int()
}

func TestZeroCall(t *testing.T) {
	defer func() { recover() }()
	z := Zero{}
	z.Call()
}

func TestZeroIter(t *testing.T) {
	defer func() { recover() }()
	z := Zero{}
	z.Iterator()
}

func TestZeroLen(t *testing.T) {
	defer func() { recover() }()
	z := Zero{}
	_ = z.Len()
}