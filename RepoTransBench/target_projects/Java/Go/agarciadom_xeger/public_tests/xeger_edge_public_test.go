package public_tests

import (
	"math/rand"
	"testing"
	"agarciadom_xeger/xeger"
)

func expectPanic(t *testing.T, f func(), expectedErr string) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for: %s", expectedErr)
		}
	}()
	f()
}

func TestXegerEdgePublic_InvalidRegexThrowsException(t *testing.T) {
	expectPanic(t, func() {
		xeger.NewXegerWithRand("(abc", rand.New(rand.NewSource(99)))
	}, "Invalid regex (unclosed parens)")
}

func generate(x *xeger.Xeger, min, max int) (string, error) {
	return x.GenerateWithBounds(min, max)
}

func TestXegerEdgePublic_GenerateMinEqualsMax(t *testing.T) {
	g := xeger.NewXegerWithRand("[cd]{2,2}e", rand.New(rand.NewSource(77)))
	s, err := generate(g, 3, 3)
	if err != nil {
		t.Fatalf("Error in generate: %v", err)
	}
	if len(s) != 3 {
		t.Errorf("Expected length 3, got %d", len(s))
	}
}

func TestXegerEdgePublic_GenerateTooShortThrowsException(t *testing.T) {
	g := xeger.NewXegerWithRand("xyz", rand.New(rand.NewSource(13)))
	_, err := generate(g, 5, 5)
	if err == nil {
		t.Fatalf("Expected FailedRandomWalkError but no error was thrown")
	}
}

func TestXegerEdgePublic_GenerateAcceptOnFirstStep(t *testing.T) {
	g := xeger.NewXegerWithRand("b*", rand.New(rand.NewSource(11)))
	s, err := generate(g, 0, 0)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(s) != 0 {
		t.Errorf("Expected length=0, got %d", len(s))
	}
}

func TestXegerEdgePublic_GenerateNormalFlow(t *testing.T) {
	g := xeger.NewXegerWithRand("abc|xyz", rand.New(rand.NewSource(3)))
	s := g.Generate()
	if s != "abc" && s != "xyz" {
		t.Errorf("Output was '%s', expected 'abc' or 'xyz'", s)
	}
}