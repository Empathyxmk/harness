package original

import (
	"errors"
	"testing"

	"yourmodule/rajinipp/lexer"
	"yourmodule/rajinipp/exceptions"
)

func TestLexerAddAndGetTokens(t *testing.T) {
	tokens := map[string]string{"NUM": "\\d+", "PLUS": "\\+"}
	lex, err := lexer.NewLexer(tokens)
	if err != nil {
		t.Fatalf("lexer.NewLexer error: %v", err)
	}
	if lex == nil || !lex.HasLexMethod() {
		t.Fatalf("Lexer should have a Lex method")
	}
	tokList := lex.Lex("3 + 5")
	expected := map[string]bool{"NUM": true, "PLUS": true}
	seen := map[string]bool{}
	for _, tok := range tokList {
		seen[tok.Name] = true
	}
	for k := range expected {
		if !seen[k] {
			t.Errorf("Token %s was not produced by lexer", k)
		}
	}
}

func TestLexerIgnoreCommentsAndWhitespace(t *testing.T) {
	tokens := map[string]string{"ID": "[a-zA-Z_]+", "EQ": "="}
	lex, err := lexer.NewLexer(tokens)
	if err != nil {
		t.Fatalf("lexer.NewLexer error: %v", err)
	}
	code := "foo = bar   !! this is a comment\nbaz=qux"
	tokList := lex.Lex(code)
	expected := []string{"ID", "EQ", "ID", "ID", "EQ", "ID"}
	got := []string{}
	for _, tok := range tokList {
		got = append(got, tok.Name)
	}
	for i, e := range expected {
		if got[i] != e {
			t.Errorf("Expected token %s at index %d, got %s", e, i, got[i])
		}
	}
}

func TestBreakException(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Should have panicked with BreakException")
		} else {
			_, ok := r.(exceptions.BreakException)
			if !ok {
				t.Errorf("Expected BreakException, got %T", r)
			}
		}
	}()
	panic(exceptions.BreakException{Message: "Break now"})
}

func TestReturnExceptionValue(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Should have panicked with ReturnException")
		} else {
			re, ok := r.(exceptions.ReturnException)
			if !ok {
				t.Fatalf("Expected ReturnException, got %T", r)
			}
			if re.ReturnValue != 42 {
				t.Fatalf("Return value mismatch, got %v", re.ReturnValue)
			}
			if !errors.Is(errors.New(re.Error()), errors.New("Return!")) && re.Error() != "Return!" {
				t.Errorf("Exception message mismatch, got %s", re.Error())
			}
		}
	}()
	panic(exceptions.ReturnException{Message: "Return!", ReturnValue: 42})
}