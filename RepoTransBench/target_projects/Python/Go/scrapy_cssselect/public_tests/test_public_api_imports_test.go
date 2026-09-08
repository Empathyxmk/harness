package public_tests

import (
	"testing"

	"scrapy_cssselect/cssselect"
)

func TestImportSomeAttrsPublic(t *testing.T) {
	subset := []string{
		"GenericTranslator",
		"parse",
		"SelectorError",
		"Selector",
		"HTMLTranslator",
	}
	for _, attr := range subset {
		found := false
		switch attr {
		case "GenericTranslator":
			_ = cssselect.GenericTranslator{}
			found = true
		case "HTMLTranslator":
			_ = cssselect.HTMLTranslator{}
			found = true
		case "parse":
			_, err := cssselect.Parse("")
			_ = err
			found = true
		case "SelectorError":
			_ = cssselect.SelectorError{}
			found = true
		case "Selector":
			_ = cssselect.Selector{}
			found = true
		default:
			found = false
		}
		if !found {
			t.Errorf("cssselect missing attribute %s", attr)
		}
	}
}

func TestVersionPublic(t *testing.T) {
	if cssselect.VERSION == "" {
		t.Error("cssselect.VERSION is empty string")
	}
	if v, ok := interface{}(cssselect.__version__).(string); !ok || len(v) == 0 {
		t.Errorf("cssselect.__version__ is not non-empty string, got %#v", cssselect.__version__)
	}
}