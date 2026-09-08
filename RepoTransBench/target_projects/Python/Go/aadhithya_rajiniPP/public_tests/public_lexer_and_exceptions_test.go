package public_tests

import (
	"strings"
	"testing"
)

func TestPublicLexerTokenizationForIdentifier(t *testing.T) {
	tokens, err := readYML("rajinipp/token.yml")
	if err != nil {
		t.Fatalf("Failed to read yml: %v", err)
	}
	lex := NewLexer(tokens)
	out := lex.Lex("varX1 = 9")
	found := false
	for _, tok := range out {
		if tok.Name == "ID" {
			found = true
		}
	}
	if !found {
		t.Error("Should have an 'ID' token in the tokenization result")
	}
}

func TestPublicLexerIgnoresComments(t *testing.T) {
	tokens, err := readYML("rajinipp/token.yml")
	if err != nil {
		t.Fatalf("Failed to read yml: %v", err)
	}
	lex := NewLexer(tokens)
	code := "num = 2  !! this is a comment\nprint num"
	out := lex.Lex(code)
	builder := &strings.Builder{}
	for _, tok := range out {
		if tok.Value != "" {
			builder.WriteString(tok.Value)
			builder.WriteString(" ")
		}
	}
	if strings.Contains(builder.String(), "!!") {
		t.Errorf("Lexer should ignore comments; found '!!' in %q", builder.String())
	}
}

func TestPublicLexerRaiseFileException(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Should have panicked for missing file")
		}
	}()
	_, _ = readYML("no_such_file.yaml")
}

// You would implement NewLexer, readYML using your Go implementation, as well as adequate Tok/Token types for lexing.