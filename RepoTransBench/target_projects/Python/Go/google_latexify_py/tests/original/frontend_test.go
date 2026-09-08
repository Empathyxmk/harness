// Code generated from src/latexify/frontend_test.py
package original

import (
	"testing"
	"github.com/yourusername/googlelatexify/latexify/frontend"
)

func TestFunction(t *testing.T) {
	f := func(x int) int { return x }
	// Simulated latexified strings:
	latexWithoutFlag := "x"
	latexWithFlag := "f(x) = x"
	
	// Simulate: latexified := frontend.Function(f)
	latexified := frontend.Function(f)
	if latexified.String() != latexWithFlag {
		t.Errorf("Expected %s, got %s", latexWithFlag, latexified.String())
	}
	if s := latexified.Latex(); s != "$$ \\displaystyle "+latexWithFlag+" $$" {
		t.Errorf("Expected latex repr with function, got %v", s)
	}

	latexified2 := frontend.FunctionWithOption(f, frontend.Opt{UseSignature: false})
	if latexified2.String() != latexWithoutFlag {
		t.Errorf("Expected %s, got %s", latexWithoutFlag, latexified2.String())
	}
	if s := latexified2.Latex(); s != "$$ \\displaystyle "+latexWithoutFlag+" $$" {
		t.Errorf("Latexified2 wrong latex: %v", s)
	}

	latexified3 := frontend.FunctionWithOptFunc(f, frontend.Opt{UseSignature: false})
	if latexified3.String() != latexWithoutFlag {
		t.Errorf("Expected %s, got %s", latexWithoutFlag, latexified3.String())
	}
	if s := latexified3.Latex(); s != "$$ \\displaystyle "+latexWithoutFlag+" $$" {
		t.Errorf("Latexified3 wrong latex: %v", s)
	}
}

func TestExpression(t *testing.T) {
	f := func(x int) int { return x }
	latexWithoutFlag := "x"
	latexWithFlag := "f(x) = x"
	
	latexified := frontend.Expression(f)
	if latexified.String() != latexWithoutFlag {
		t.Errorf("Expected %s, got %s", latexWithoutFlag, latexified.String())
	}
	if s := latexified.Latex(); s != "$$ \\displaystyle "+latexWithoutFlag+" $$" {
		t.Errorf("Latexified wrong latex: %v", s)
	}

	latexified2 := frontend.ExpressionWithOption(f, frontend.Opt{UseSignature: true})
	if latexified2.String() != latexWithFlag {
		t.Errorf("Expected %s, got %s", latexWithFlag, latexified2.String())
	}
	if s := latexified2.Latex(); s != "$$ \\displaystyle "+latexWithFlag+" $$" {
		t.Errorf("Latexified2 wrong latex: %v", s)
	}

	latexified3 := frontend.ExpressionWithOptFunc(f, frontend.Opt{UseSignature: true})
	if latexified3.String() != latexWithFlag {
		t.Errorf("Expected %s, got %s", latexWithFlag, latexified3.String())
	}
	if s := latexified3.Latex(); s != "$$ \\displaystyle "+latexWithFlag+" $$" {
		t.Errorf("Latexified3 wrong latex: %v", s)
	}
}