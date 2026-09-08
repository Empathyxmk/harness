package public_tests

import (
	"testing"
	"eatonphil_pj/pj/lexer"
)

func TestLexNumberSimplePublic(t *testing.T) {
	tok, rest := lexer.LexNumber("222abc")
	if tok != 222 {
		t.Errorf("expected 222, got %v", tok)
	}
	if rest != "abc" {
		t.Errorf("expected abc, got %q", rest)
	}
}

func TestLexNumberDecimalPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("99.123z")
	if !almostEqual(tok, 99.123) {
		t.Errorf("expected 99.123, got %v", tok)
	}
	if rest != "z" {
		t.Errorf("expected z, got %q", rest)
	}
}

func TestLexNumberNegativePublic(t *testing.T) {
	tok, rest := lexer.LexNumber("-657tail")
	if tok != -657 {
		t.Errorf("expected -657, got %v", tok)
	}
	if rest != "tail" {
		t.Errorf("expected tail, got %q", rest)
	}
}

func TestLexNumberZeroPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("0____")
	if tok != 0 {
		t.Errorf("expected 0, got %v", tok)
	}
	if rest != "____" {
		t.Errorf("expected ____ got %q", rest)
	}
}

func TestLexNumberLeadingZeroesPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("0005!")
	if tok != 0 {
		t.Errorf("expected 0, got %v", tok)
	}
	if rest != "005!" {
		t.Errorf("expected 005! got %q", rest)
	}
}

func TestLexEscapeSingleEscapedPublic(t *testing.T) {
	tok, rest := lexer.LexEscaped(`"f\nulio"rest`)
	if tok != "f\\nulio" {
		t.Errorf("expected 'f\\nulio', got %v", tok)
	}
	if rest != "rest" {
		t.Errorf("expected rest got %q", rest)
	}
}

func TestLexEscapeQuotesPublic(t *testing.T) {
	tok, rest := lexer.LexEscaped(`"abc\"def"tail`)
	if tok != `abc\"def` {
		t.Errorf("expected 'abc\\\"def', got %v", tok)
	}
	if rest != "tail" {
		t.Errorf("expected tail got %q", rest)
	}
}

func TestLexEscapeHexPublic(t *testing.T) {
	tok, rest := lexer.LexEscaped(`"\x48abc"x`)
	if tok != `\x48abc` {
		t.Errorf("expected '\\x48abc', got %v", tok)
	}
	if rest != "x" {
		t.Errorf("expected x got %q", rest)
	}
}

func TestLexEscapeUnicodePublic(t *testing.T) {
	tok, rest := lexer.LexEscaped(`"\u0048"abc`)
	if tok != `\u0048` {
		t.Errorf("expected '\\u0048', got %v", tok)
	}
	if rest != "abc" {
		t.Errorf("expected abc got %q", rest)
	}
}

func TestLexNumberFloatExponentPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("18.12e2!")
	if !almostEqual(tok, 1812) {
		t.Errorf("expected 1812, got %v", tok)
	}
	if rest != "!" {
		t.Errorf("expected ! got %q", rest)
	}
}

func TestLexNumberNegativeExponentPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("45e-1Q")
	if !almostEqual(tok, 4.5) {
		t.Errorf("expected 4.5, got %v", tok)
	}
	if rest != "Q" {
		t.Errorf("expected Q got %q", rest)
	}
}

func TestLexNumberLargeExponentPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("2.5e3and")
	if !almostEqual(tok, 2500) {
		t.Errorf("expected 2500, got %v", tok)
	}
	if rest != "and" {
		t.Errorf("expected and got %q", rest)
	}
}

func TestLexNumberPlusExponentPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("6e+2zzz")
	if !almostEqual(tok, 600) {
		t.Errorf("expected 600, got %v", tok)
	}
	if rest != "zzz" {
		t.Errorf("expected zzz got %q", rest)
	}
}

func TestLexNumberValidExponentOtherPublic(t *testing.T) {
	tok, rest := lexer.LexNumber("5e1X")
	if !almostEqual(tok, 50) {
		t.Errorf("expected 50, got %v", tok)
	}
	if rest != "X" {
		t.Errorf("expected X got %q", rest)
	}
}

func TestLexBoolTruePublic(t *testing.T) {
	tok, rest := lexer.LexBool("truee")
	if tok != true {
		t.Errorf("expected true, got %v", tok)
	}
	if rest != "e" {
		t.Errorf("expected e got %q", rest)
	}
}

func TestLexBoolFalsePublic(t *testing.T) {
	tok, rest := lexer.LexBool("falsest")
	if tok != false {
		t.Errorf("expected false, got %v", tok)
	}
	if rest != "st" {
		t.Errorf("expected st got %q", rest)
	}
}

func TestLexBoolInvalidPublic(t *testing.T) {
	tok, _ := lexer.LexBool("turtle")
	if tok != nil && tok != false {
		t.Errorf("expected nil/false, got %v", tok)
	}
}

func TestLexNullPublic(t *testing.T) {
	tok, rest := lexer.LexNull("nullify")
	if tok != nil && tok != false {
		t.Errorf("expected nil/false, got %v", tok)
	}
	if rest != "ify" {
		t.Errorf("expected ify got %q", rest)
	}
}

func TestLexNullInvalidPublic(t *testing.T) {
	tok, _ := lexer.LexNull("notnull")
	if tok != nil && tok != false {
		t.Errorf("expected nil/false, got %v", tok)
	}
}

func TestNextLexedPublic(t *testing.T) {
	toks := []interface{}{}
	program := "12 \"abc\" true null"
	for len(program) > 0 {
		val, next := lexer.NextLexed(program)
		toks = append(toks, val)
		program = trimSpace(next)
		if program == "" {
			break
		}
	}
	want := []interface{}{12, "abc", true, nil}
	if len(toks) != len(want) {
		t.Errorf("expected %v tokens, got %v", len(want), len(toks))
	}
	for i, v := range want {
		if toks[i] != v {
			t.Errorf("at %d: expected %v, got %v", i, v, toks[i])
		}
	}
}

func TestNextLexedFloatPublic(t *testing.T) {
	val, rest := lexer.NextLexed("3.51hello")
	numB, ok := val.(float64)
	if !ok {
		t.Errorf("expected float64, got %T", val)
		return
	}
	if !almostEqual(numB, 3.51) {
		t.Errorf("expected 3.51, got %v", numB)
	}
	if rest != "hello" {
		t.Errorf(`expected "hello", got %q`, rest)
	}
}

// Helper functions

func almostEqual(val interface{}, target float64) bool {
	num, ok := val.(float64)
	if !ok {
		return false
	}
	diff := num - target
	if diff < 0 {
		diff = -diff
	}
	return diff < 1e-6
}

func trimSpace(s string) string {
	i := 0
	n := len(s)
	// left trim
	for i < n && (s[i] == ' ' || s[i] == '\t' || s[i] == '\n' || s[i] == '\r') {
		i++
	}
	return s[i:]
}