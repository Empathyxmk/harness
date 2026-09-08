package original

import (
	"strings"
	"testing"
	"vasco"
)

func TestContextEquals(t *testing.T) {
	c1 := &vasco.Context{Method: "A", ID: 1}
	c2 := &vasco.Context{Method: "A", ID: 1}
	c3 := &vasco.Context{Method: "B", ID: 2}

	if !c1.Equal(c2) {
		t.Error("Context should equal")
	}
	if c1.Equal(c3) {
		t.Error("Context should not equal")
	}
}

func TestContextHashCode(t *testing.T) {
	c1 := &vasco.Context{Method: "A", ID: 1}
	c2 := &vasco.Context{Method: "A", ID: 1}

	if c1.Hash() != c2.Hash() {
		t.Error("Hash codes must match")
	}
}

func TestNullContext(t *testing.T) {
	c1 := &vasco.Context{Method: nil, ID: 0}
	c2 := &vasco.Context{Method: nil, ID: 0}
	if !c1.Equal(c2) {
		t.Error("Contexts with nil Method should equal")
	}
}

func TestContextToString(t *testing.T) {
	c1 := &vasco.Context{Method: "Method", ID: 5}
	if !strings.Contains(c1.String(), "Method") {
		t.Error("String should contain method name")
	}
}