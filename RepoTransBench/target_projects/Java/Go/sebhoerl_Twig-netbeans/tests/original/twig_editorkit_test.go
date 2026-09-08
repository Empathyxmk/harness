package original

import (
	"testing"

	"twigmodule/tests"
)

func TestContentType(t *testing.T) {
	kit := tests.NewTwigEditorKit()
	if ct := kit.GetContentType(); ct != "text/twig" {
		t.Errorf("Expected content type 'text/twig', got '%s'", ct)
	}
}

func TestCreateDefaultDocument(t *testing.T) {
	kit := tests.NewTwigEditorKit()
	doc := kit.CreateDefaultDocument()
	if doc == nil {
		t.Errorf("Expected non-nil document")
	}
}