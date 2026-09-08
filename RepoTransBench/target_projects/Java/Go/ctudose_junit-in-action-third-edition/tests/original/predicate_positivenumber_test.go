package original

import "testing"

type PositiveNumberPredicate struct{}

func (p *PositiveNumberPredicate) Test(n int) bool {
	return n > 0
}

func TestWithPositiveNumber(t *testing.T) {
	p := &PositiveNumberPredicate{}
	if !p.Test(10) {
		t.Error("Should be true for a positive number")
	}
}

func TestWithZero(t *testing.T) {
	p := &PositiveNumberPredicate{}
	if p.Test(0) {
		t.Error("Should be false for zero")
	}
}

func TestWithNegativeNumber(t *testing.T) {
	p := &PositiveNumberPredicate{}
	if p.Test(-5) {
		t.Error("Should be false for a negative number")
	}
}