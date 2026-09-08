package public

import (
	"testing"
)

type PubUniqueStringGenerator struct {
	prefix string
	length int
	counter int
}

func NewPubUniqueStringGenerator(length int) *PubUniqueStringGenerator {
	return &PubUniqueStringGenerator{"", length, 0}
}

func (g *PubUniqueStringGenerator) get() string {
	out := ""
	if g.prefix != "" {
		out = g.prefix
	}
	num := itoa(g.counter)
	for len(out)+len(num) < g.length {
		out += "x"
	}
	out += num
	g.counter++
	return out
}

func TestUniqueStringGeneratorPublic_MinLength(t *testing.T) {
	gen := NewPubUniqueStringGenerator(5)
	s := gen.get()
	if len(s) != 5 {
		t.Errorf("expected length 5, got %d", len(s))
	}
}

func TestUniqueStringGeneratorPublic_Unique(t *testing.T) {
	gen := NewPubUniqueStringGenerator(6)
	s1 := gen.get()
	s2 := gen.get()
	if s1 == s2 {
		t.Errorf("expected different strings")
	}
}