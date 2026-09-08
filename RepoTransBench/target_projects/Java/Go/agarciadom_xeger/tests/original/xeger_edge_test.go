package original

import (
	"math/rand"
	"testing"
	"agarciadom_xeger/xeger"
)

// Helper to expect a panic
func expectPanic(t *testing.T, f func(), expectedErr string) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for %s, but code did not panic", expectedErr)
		}
	}()
	f()
}

func TestXegerEdge_InvalidRegexThrowsException(t *testing.T) {
	expectPanic(t, func() {
		xeger.NewXegerWithRand("[A-Z", rand.New(rand.NewSource(1))) // Unclosed bracket
	}, "Invalid regex")
}

// Example GenerateWithBounds stub for stubbing .generate(min, max)
func generate(x *xeger.Xeger, min, max int) (string, error) {
	return x.GenerateWithBounds(min, max)
}

func TestXegerEdge_GenerateMinEqualsMax(t *testing.T) {
	g := xeger.NewXegerWithRand("[ab]{3,3}c", rand.New(rand.NewSource(42)))
	s, err := generate(g, 4, 4)
	if err != nil {
		t.Fatalf("Error in generate: %v", err)
	}
	if len(s) != 4 {
		t.Errorf("Expected length 4, got %d", len(s))
	}
	// Regex match, placeholder: always true
	// TODO: proper regex validation on output
}

func TestXegerEdge_GenerateTooShortThrowsException(t *testing.T) {
	g := xeger.NewXegerWithRand("abc", rand.New(rand.NewSource(42)))
	_, err := generate(g, 4, 4)
	if err == nil {
		t.Fatalf("Expected FailedRandomWalkError but no error was thrown")
	}
}

func TestXegerEdge_GenerateAcceptOnFirstStep(t *testing.T) {
	g := xeger.NewXegerWithRand("a*", rand.New(rand.NewSource(42)))
	s, err := generate(g, 0, 0)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(s) != 0 {
		t.Errorf("Expected length=0, got %d", len(s))
	}
}

func TestXegerEdge_GenerateNormalFlow(t *testing.T) {
	g := xeger.NewXegerWithRand("abc|def", rand.New(rand.NewSource(1)))
	s := g.Generate()
	ok := s == "abc" || s == "def"
	if !ok {
		t.Errorf("Output was '%s', expected 'abc' or 'def'", s)
	}
}