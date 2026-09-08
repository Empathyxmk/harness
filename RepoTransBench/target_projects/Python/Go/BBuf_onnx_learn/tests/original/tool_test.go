package original

import (
	"testing"
	"bbuf_onnx_learn/tools"
)

func TestAdd(t *testing.T) {
	if got := tools.Add(1, 2); got != 3 {
		t.Errorf("Add(1,2) = %v; want 3", got)
	}
	if got := tools.Add(-2, 2); got != 0 {
		t.Errorf("Add(-2,2) = %v; want 0", got)
	}
	if got := tools.Add(0, 0); got != 0 {
		t.Errorf("Add(0,0) = %v; want 0", got)
	}
}

func TestSub(t *testing.T) {
	if got := tools.Sub(3, 2); got != 1 {
		t.Errorf("Sub(3,2) = %v; want 1", got)
	}
	if got := tools.Sub(-1, 1); got != -2 {
		t.Errorf("Sub(-1,1) = %v; want -2", got)
	}
}

func TestMul(t *testing.T) {
	if got := tools.Mul(3, 2); got != 6 {
		t.Errorf("Mul(3,2) = %v; want 6", got)
	}
	if got := tools.Mul(0, 8); got != 0 {
		t.Errorf("Mul(0,8) = %v; want 0", got)
	}
}

func TestDiv(t *testing.T) {
	if got, err := tools.Div(6, 3); err != nil || got != 2 {
		t.Errorf("Div(6,3) = (%v,%v); want (2,nil)", got, err)
	}
	if _, err := tools.Div(3, 0); err == nil {
		t.Errorf("Div(3,0) expected error for division by zero, got nil")
	}
}

func TestToolClass(t *testing.T) {
	toolObj := tools.NewTool()
	if got := toolObj.Multiply(2, 3); got != 6 {
		t.Errorf("Tool.Multiply(2,3) = %v; want 6", got)
	}
	if got := toolObj.Identity(10); got != 10 {
		t.Errorf("Tool.Identity(10) = %v; want 10", got)
	}
	// In Go, all methods are callable, so we don't need to check for callability
}