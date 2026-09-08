package original

import (
	"testing"
	"twigmodule/tests"
)

func TestLanguageNotNull(t *testing.T) {
	lang := tests.Language()
	if lang == "" {
		t.Errorf("Expected non-empty language")
	}
}