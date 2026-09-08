package original

import (
	"testing"
)

func ReverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func TestReverseString(t *testing.T) {
	if ReverseString("tiddl") != "lddit" {
		t.Errorf("ReverseString(\"tiddl\") = %q, want \"lddit\"", ReverseString("tiddl"))
	}
	if ReverseString("A") != "A" {
		t.Errorf("ReverseString(\"A\") = %q, want \"A\"", ReverseString("A"))
	}
	if ReverseString("") != "" {
		t.Errorf("ReverseString(\"\") = %q, want \"\"", ReverseString(""))
	}
}