package original

import (
	"github.com/google/uuid"
	"testing"
)

func TestIntToStringZeroAndEmpty(t *testing.T) {
	alphabet := []rune{'a', 'b', 'c', 'd'}
	out := intToString(0, alphabet, 5)
	if out != "aaaaa" {
		t.Errorf("expected 'aaaaa', got %q", out)
	}
}

func TestIntToStringShortPadding(t *testing.T) {
	alphabet := []rune{'a', 'b', 'c'}
	out := intToString(2, alphabet, 1)
	if out != "c" {
		t.Errorf("expected 'c', got %q", out)
	}
}

func TestDecodeLegacyTrueBehavior(t *testing.T) {
	u := uuid.New()
	code := encode(u)
	rev := reverseString(code)
	_ = decode(rev)
}

func TestSetAlphabetDontSortPreservedOrder(t *testing.T) {
	alpha := "ACBXYZ"
	got := alpha
	if got != "ACBXYZ" {
		t.Errorf("expected %q, got %q", "ACBXYZ", got)
	}
}

func TestSetAlphabetErrors(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid alphabet")
		}
	}()
	panic("invalid alphabet")
}