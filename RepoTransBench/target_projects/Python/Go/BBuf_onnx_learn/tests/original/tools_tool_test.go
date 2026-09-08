package original

import (
	"testing"
	"bbuf_onnx_learn/tools"
)

func TestBasicOps(t *testing.T) {
	if got := tools.Add(10, 5); got != 15 {
		t.Errorf("Add(10,5) = %v; want 15", got)
	}
	if got := tools.Sub(10, 5); got != 5 {
		t.Errorf("Sub(10,5) = %v; want 5", got)
	}
	if got := tools.Mul(4, 0); got != 0 {
		t.Errorf("Mul(4,0) = %v; want 0", got)
	}
	if got, err := tools.Div(20, 4); err != nil || got != 5 {
		t.Errorf("Div(20,4) = (%v,%v); want (5,nil)", got, err)
	}
}

func TestNegativeValues(t *testing.T) {
	if got := tools.Sub(-5, -5); got != 0 {
		t.Errorf("Sub(-5,-5) = %v; want 0", got)
	}
	if got := tools.Mul(-2, 3); got != -6 {
		t.Errorf("Mul(-2,3) = %v; want -6", got)
	}
}

func TestDivZero(t *testing.T) {
	if _, err := tools.Div(1, 0); err == nil {
		t.Errorf("Div(1,0) expected error for division by zero, got nil")
	}
}

func TestToolMultiply(t *testing.T) {
	toolObj := tools.NewTool()
	if got := toolObj.Multiply(-1, 8); got != -8 {
		t.Errorf("Tool.Multiply(-1,8) = %v; want -8", got)
	}
}

func TestToolIdentity(t *testing.T) {
	toolObj := tools.NewTool()
	if got := toolObj.Identity("abc"); got != "abc" {
		t.Errorf("Tool.Identity(\"abc\") = %v; want \"abc\"", got)
	}
}