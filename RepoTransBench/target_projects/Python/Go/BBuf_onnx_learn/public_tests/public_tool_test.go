package public_tests

import (
	"testing"
	"bbuf_onnx_learn/tools"
)

func TestAdd(t *testing.T) {
	if got := tools.Add(5, 7); got != 12 {
		t.Errorf("Add(5,7) = %v; want 12", got)
	}
	if got := tools.Add(-3, 3); got != 0 {
		t.Errorf("Add(-3,3) = %v; want 0", got)
	}
	if got := tools.Add(10, -10); got != 0 {
		t.Errorf("Add(10,-10) = %v; want 0", got)
	}
}

func TestSub(t *testing.T) {
	if got := tools.Sub(10, 2); got != 8 {
		t.Errorf("Sub(10,2) = %v; want 8", got)
	}
	if got := tools.Sub(-10, 5); got != -15 {
		t.Errorf("Sub(-10,5) = %v; want -15", got)
	}
}

func TestMul(t *testing.T) {
	if got := tools.Mul(7, 3); got != 21 {
		t.Errorf("Mul(7,3) = %v; want 21", got)
	}
	if got := tools.Mul(-4, 2); got != -8 {
		t.Errorf("Mul(-4,2) = %v; want -8", got)
	}
}

func TestDiv(t *testing.T) {
	if got, err := tools.Div(8, 2); err != nil || got != 4 {
		t.Errorf("Div(8,2) = (%v,%v); want (4,nil)", got, err)
	}
	if _, err := tools.Div(-4, 0); err == nil {
		t.Errorf("Div(-4,0) expected error for division by zero, got nil")
	}
}

func TestToolClass(t *testing.T) {
	toolObj := tools.NewTool()
	if got := toolObj.Multiply(4, -2); got != -8 {
		t.Errorf("Tool.Multiply(4,-2) = %v; want -8", got)
	}
	if got := toolObj.Identity(0); got != 0 {
		t.Errorf("Tool.Identity(0) = %v; want 0", got)
	}
}