package original

import (
	"testing"
	"errors"
	"reflect"
	"eatonphil_pj/pj/lexer"
)

func TestLexStringSimple(t *testing.T) {
	tok, rest, err := lexer.LexString(`"abc"`)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if tok != "abc" {
		t.Errorf("expected 'abc', got %v", tok)
	}
	if rest != "" {
		t.Errorf("expected empty rest, got %q", rest)
	}
	_, _, err = lexer.LexString(`"abc`)
	if err == nil {
		t.Error("expected error for no end quote, got none")
	}
}

func TestLexStringFail(t *testing.T) {
	tok, rest, err := lexer.LexString("notstring")
	if tok != "" && tok != "<nil>" {
		t.Errorf("expected '', got %v", tok)
	}
	if rest != "notstring" {
		t.Errorf("expected rest 'notstring', got %q", rest)
	}
}

func TestLexNumberInt(t *testing.T) {
	tok, rest := lexer.LexNumber("123 end")
	if tok != 123 {
		t.Errorf("expected 123, got %v", tok)
	}
	if rest != " end" {
		t.Errorf(`expected " end", got %q`, rest)
	}
	tok, rest = lexer.LexNumber("-55 foo")
	if tok != -55 {
		t.Errorf("expected -55, got %v", tok)
	}
	if rest != " foo" {
		t.Errorf(`expected " foo", got %q`, rest)
	}
}

func TestLexNumberFloat(t *testing.T) {
	tok, rest := lexer.LexNumber("3.14rest")
	if !almostEqual(tok, 3.14) {
		t.Errorf("expected 3.14, got %v", tok)
	}
	if rest != "rest" {
		t.Errorf(`expected "rest", got %q`, rest)
	}
	tok, rest = lexer.LexNumber("abc")
	if tok != nil && tok != 0 {
		t.Errorf("expected nil, got %v", tok)
	}
	if rest != "abc" {
		t.Errorf(`expected "abc", got %q`, rest)
	}
}

func TestLexNumberValidExponent(t *testing.T) {
	tok, rest := lexer.LexNumber("1.23e2foo")
	if !almostEqual(tok, 1.23e2) {
		t.Errorf("expected 1.23e2, got %v", tok)
	}
	if rest != "foo" {
		t.Errorf(`expected "foo", got %q`, rest)
	}
	tok, rest = lexer.LexNumber("-3.2e2z")
	if !almostEqual(tok, -3.2e2) {
		t.Errorf("expected -3.2e2, got %v", tok)
	}
	if rest != "z" {
		t.Errorf(`expected "z", got %q`, rest)
	}
}

func TestLexBoolTrueFalse(t *testing.T) {
	tok, rest := lexer.LexBool("trueabc")
	if tok != true {
		t.Errorf("expected true, got %v", tok)
	}
	if rest != "abc" {
		t.Errorf(`expected "abc", got %q`, rest)
	}
	tok, rest = lexer.LexBool("falsex")
	if tok != false {
		t.Errorf("expected false, got %v", tok)
	}
	if rest != "x" {
		t.Errorf(`expected "x", got %q`, rest)
	}
	tok, rest = lexer.LexBool("null")
	if tok != nil && tok != false {
		t.Errorf("expected nil, got %v", tok)
	}
	if rest != "null" {
		t.Errorf(`expected "null", got %q`, rest)
	}
}

func TestLexNull(t *testing.T) {
	tok, rest := lexer.LexNull("nullvalue")
	if tok != true {
		t.Errorf("expected true, got %v", tok)
	}
	if rest != "value" {
		t.Errorf(`expected "value", got %q`, rest)
	}
	tok, rest = lexer.LexNull("none")
	if tok != nil && tok != false {
		t.Errorf("expected nil, got %v", tok)
	}
	if rest != "none" {
		t.Errorf(`expected "none", got %q`, rest)
	}
}

func TestLexSingleWhitespace(t *testing.T) {
	got := lexer.Lex(" ")
	want := []interface{}{}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestLexSyntaxTokens(t *testing.T) {
	for _, syntax := range []string{",", ":", "[", "]", "{", "}"} {
		got := lexer.Lex(syntax)
		if len(got) != 1 || got[0] != syntax {
			t.Errorf("expected [%s], got %v", syntax, got)
		}
	}
}

func TestLexCombined(t *testing.T) {
	s := `{"foo": [123, "bar", false, null]}`
	got := lexer.Lex(s)
	want := []interface{}{
		"{", "foo", ":", "[", 123, ",", "bar", ",", false, ",", nil, "]", "}",
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestLexBadChar(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic due to invalid char, got none")
		}
	}()
	lexer.Lex("$notvalid")
}

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