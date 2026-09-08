package tests

import (
	"testing"
)

type UniqueStringGenerator struct {
	prefix string
	length int
	counter int
}

func NewUniqueStringGenerator(length int) *UniqueStringGenerator {
	return &UniqueStringGenerator{"", length, 0}
}

func (g *UniqueStringGenerator) get() string {
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

func (g *UniqueStringGenerator) isOffensive(s string) bool {
	offensive := []string{"shit", "fvck", "sh1t", "1a552"}
	for _, word := range offensive {
		if containsInsensitive(s, word) {
			return true
		}
	}
	return false
}

func containsInsensitive(str, substr string) bool {
	return len(str) >= len(substr) && (str == substr ||
		len(str) > 0 && containsInsensitive(str[1:], substr))
}

func TestUniqueStringGenerator_HappyPath(t *testing.T) {
	gen := NewUniqueStringGenerator(8)
	s1 := gen.get()
	s2 := gen.get()
	if len(s1) != 8 {
		t.Errorf("expected s1 to have length 8, got %v", len(s1))
	}
	if len(s2) != 8 {
		t.Errorf("expected s2 to have length 8, got %v", len(s2))
	}
	if s1 == s2 {
		t.Errorf("expected s1 and s2 to be different")
	}
}

func TestUniqueStringGenerator_Inoffensive(t *testing.T) {
	gen := NewUniqueStringGenerator(8)
	if gen.isOffensive("puppies") {
		t.Errorf("expected puppies not to be offensive")
	}
	if gen.isOffensive("muffins") {
		t.Errorf("expected muffins not to be offensive")
	}
	if !gen.isOffensive("fvck") {
		t.Errorf("expected fvck to be offensive")
	}
	if !gen.isOffensive("abcshitdef") {
		t.Errorf("expected abcshitdef to be offensive")
	}
	if !gen.isOffensive("abcsh1tdef") {
		t.Errorf("expected abcsh1tdef to be offensive")
	}
	if !gen.isOffensive("1a552") {
		t.Errorf("expected 1a552 to be offensive")
	}
}