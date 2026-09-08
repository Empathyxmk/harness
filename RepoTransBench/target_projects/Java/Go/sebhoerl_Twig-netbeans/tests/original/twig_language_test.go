package original

import (
	"testing"
	"twigmodule/tests"
)

func TestDisplayName(t *testing.T) {
	lang := &tests.TwigLanguage{}
	if lang.GetDisplayName() != "Twig" {
		t.Errorf("Expected display name 'Twig', got '%s'", lang.GetDisplayName())
	}
	if lang.GetPreferredExtension() != "twig" {
		t.Errorf("Expected extension 'twig'")
	}
}

func TestIsIdentifierChar(t *testing.T) {
	lang := &tests.TwigLanguage{}
	if !lang.IsIdentifierChar('a') {
		t.Errorf("'a' should be identifier char")
	}
	if lang.IsIdentifierChar('1') {
		t.Errorf("'1' should not be identifier char")
	}
	if lang.IsIdentifierChar('*') {
		t.Errorf("'*' should not be identifier char")
	}
}

func TestGetCompletionHandlerAndFormatter(t *testing.T) {
	lang := &tests.TwigLanguage{}
	cch := lang.GetCompletionHandler()
	if cch == nil {
		t.Error("CompletionHandler should not be nil")
	}
	formatter := lang.GetFormatter()
	if formatter == nil {
		t.Error("Formatter should not be nil")
	}
}

func TestHasStructureScannerAndHintsProvider(t *testing.T) {
	lang := &tests.TwigLanguage{}
	if !lang.HasStructureScanner() {
		t.Error("Should have structure scanner")
	}
	if lang.HasHintsProvider() {
		t.Error("Should not have hints provider")
	}
	ss := lang.GetStructureScanner()
	if ss == nil {
		t.Error("Structure scanner should not be nil")
	}
}

func TestIsUsingCustomEditorKitAndHasFormatter(t *testing.T) {
	lang := &tests.TwigLanguage{}
	if !lang.IsUsingCustomEditorKit() {
		t.Error("Should use custom editor kit")
	}
	if !lang.HasFormatter() {
		t.Error("Should have formatter")
	}
}