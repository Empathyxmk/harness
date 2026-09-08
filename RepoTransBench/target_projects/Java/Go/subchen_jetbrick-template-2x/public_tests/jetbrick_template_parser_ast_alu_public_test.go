package public_tests

import (
	"testing"
)

type ALUPub struct{}

func (ALUPub) Eval(op rune, a, b int) int {
	switch op {
	case '+':
		return a + b
	case '-':
		return a - b
	case '*':
		return a * b
	case '/':
		return a / b
	default:
		panic("unsupported")
	}
}

func TestDifferentAdditionCases(t *testing.T) {
	alu := ALUPub{}
	if alu.Eval('+', 70, 30) != 100 {
		t.Errorf("expected 100, got %d", alu.Eval('+', 70, 30))
	}
}

func TestDifferentSubtractionCases(t *testing.T) {
	alu := ALUPub{}
	if alu.Eval('-', 10, 30) != -20 {
		t.Errorf("expected -20, got %d", alu.Eval('-', 10, 30))
	}
}

func TestDifferentMultiplicationCases(t *testing.T) {
	alu := ALUPub{}
	if alu.Eval('*', 33, 30) != 990 {
		t.Errorf("expected 990, got %d", alu.Eval('*', 33, 30))
	}
}

func TestDifferentDivisionCases(t *testing.T) {
	alu := ALUPub{}
	if alu.Eval('/', 40, 10) != 4 {
		t.Errorf("expected 4, got %d", alu.Eval('/', 40, 10))
	}
}