package public_tests

import (
	"testing"
	"bbuf_onnx_learn/tools"
	"reflect"
)

func TestBasicOps(t *testing.T) {
	if got := tools.Add(20, 15); got != 35 {
		t.Errorf("Add(20,15) = %v; want 35", got)
	}
	if got := tools.Sub(30, 25); got != 5 {
		t.Errorf("Sub(30,25) = %v; want 5", got)
	}
	if got := tools.Mul(6, 1); got != 6 {
		t.Errorf("Mul(6,1) = %v; want 6", got)
	}
	if got, err := tools.Div(81, 9); err != nil || got != 9 {
		t.Errorf("Div(81,9) = (%v,%v); want (9,nil)", got, err)
	}
}

func TestNegativeValues(t *testing.T) {
	if got := tools.Sub(-10, 5); got != -15 {
		t.Errorf("Sub(-10,5) = %v; want -15", got)
	}
	if got := tools.Mul(5, -5); got != -25 {
		t.Errorf("Mul(5,-5) = %v; want -25", got)
	}
}

func TestDivZero(t *testing.T) {
	if _, err := tools.Div(-10, 0); err == nil {
		t.Errorf("Div(-10,0) expected error for division by zero, got nil")
	}
}

func TestToolMultiply(t *testing.T) {
	toolObj := tools.NewTool()
	if got := toolObj.Multiply(9, 0); got != 0 {
		t.Errorf("Tool.Multiply(9,0) = %v; want 0", got)
	}
}

func TestToolIdentity(t *testing.T) {
	toolObj := tools.NewTool()
	cmp := []interface{}{1, "x", 3}
	got := toolObj.Identity(cmp)
	if !reflect.DeepEqual(got, cmp) {
		t.Errorf("Tool.Identity([1, \"x\", 3]) = %v; want [1, \"x\", 3]", got)
	}
}