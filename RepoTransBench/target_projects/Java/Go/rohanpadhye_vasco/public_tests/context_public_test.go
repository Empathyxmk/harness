package public_tests

import (
	"strings"
	"testing"
	"vasco"
)

func TestContextEqualsDifferent(t *testing.T) {
	c1 := &vasco.Context{Method: "X", ID: 9}
	c2 := &vasco.Context{Method: "X", ID: 9}
	c3 := &vasco.Context{Method: "Y", ID: 20}
	if !c1.Equal(c2) {
		t.Error("c1 != c2")
	}
	if c1.Equal(c3) {
		t.Error("c1 == c3, expected not equal")
	}
}

func TestContextHashCodeDifferent(t *testing.T) {
	c1 := &vasco.Context{Method: "X", ID: 9}
	c2 := &vasco.Context{Method: "X", ID: 9}
	if c1.Hash() != c2.Hash() {
		t.Error("Hash mismatch")
	}
}

func TestNullContextDifferent(t *testing.T) {
	c1 := &vasco.Context{Method: nil, ID: 42}
	c2 := &vasco.Context{Method: nil, ID: 42}
	if !c1.Equal(c2) {
		t.Error("Contexts with nil method should equal")
	}
}

func TestContextToStringDifferent(t *testing.T) {
	c1 := &vasco.Context{Method: "DifferentMethod", ID: 99}
	if !strings.Contains(c1.String(), "DifferentMethod") {
		t.Error("String missing method name")
	}
}