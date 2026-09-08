package original

import (
	"testing"
	"twigmodule/tests"
)

func TestCompleteReturnsNONE(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	ccc := interface{}(nil)
	result := handler.Complete(ccc)
	if result != "NONE" {
		t.Errorf("Expected 'NONE', got '%s'", result)
	}
}

func TestDocumentIsEmpty(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	out := handler.Document(nil, nil)
	if out != "" {
		t.Errorf("Expected empty document, got '%v'", out)
	}
}

func TestResolveLinkIsNull(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	if handler.ResolveLink("foo", nil) != nil {
		t.Errorf("Expected nil when resolving link")
	}
}

func TestGetPrefixIsEmpty(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	res := handler.GetPrefix(nil, 0, true)
	if res != "" {
		t.Errorf("Expected empty string, got '%v'", res)
	}
}

func TestAutoQuery(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	res := handler.GetAutoQuery(nil, "foo")
	if res != "ALL_COMPLETION" {
		t.Errorf("Expected 'ALL_COMPLETION', got '%s'", res)
	}
}

func TestResolveTemplateVariable(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	val := handler.ResolveTemplateVariable("foo", nil, 1, "bar", map[string]interface{}{})
	if val != nil {
		t.Errorf("Expected nil for resolveTemplateVariable")
	}
}

func TestGetApplicableTemplates(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	res := handler.GetApplicableTemplates(nil, 1, 2)
	if len(res) != 0 {
		t.Errorf("Expected empty applicable templates set, got %v", res)
	}
}

func TestParameters(t *testing.T) {
	handler := tests.NewTwigCompletionHandler()
	pi := handler.Parameters(nil, 1, nil)
	if pi == nil {
		t.Error("Expected non-nil ParameterInfo")
	}
	if pi.InsertIndex != 0 {
		t.Errorf("Expected InsertIndex 0, got %d", pi.InsertIndex)
	}
	if pi.Offset != 0 {
		t.Errorf("Expected Offset 0, got %d", pi.Offset)
	}
	if len(pi.Parameters) != 0 {
		t.Errorf("Expected 0 parameters, got %d", len(pi.Parameters))
	}
}