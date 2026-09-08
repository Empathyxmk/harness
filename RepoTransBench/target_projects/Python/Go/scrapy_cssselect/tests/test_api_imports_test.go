package tests

import (
	"testing"

	"scrapy_cssselect/cssselect"
)

func TestImportAllAttrs(t *testing.T) {
	knownAttrs := []string{
		"ExpressionError",
		"FunctionalPseudoElement",
		"GenericTranslator",
		"HTMLTranslator",
		"Selector",
		"SelectorError",
		"SelectorSyntaxError",
		"parse",
	}
	for _, attr := range knownAttrs {
		found := false
		switch attr {
		case "ExpressionError":
			_ = cssselect.ExpressionError{}
			found = true
		case "FunctionalPseudoElement":
			_ = cssselect.FunctionalPseudoElement{}
			found = true
		case "GenericTranslator":
			_ = cssselect.GenericTranslator{}
			found = true
		case "HTMLTranslator":
			_ = cssselect.HTMLTranslator{}
			found = true
		case "Selector":
			_ = cssselect.Selector{}
			found = true
		case "SelectorError":
			_ = cssselect.SelectorError{}
			found = true
		case "SelectorSyntaxError":
			_ = cssselect.SelectorSyntaxError{}
			found = true
		case "parse":
			_, err := cssselect.Parse("")
			_ = err
			found = true
		default:
			found = false
		}
		if !found {
			t.Errorf("cssselect is missing attribute: %s", attr)
		}
	}
}

func TestVersion(t *testing.T) {
	if v, ok := interface{}(cssselect.VERSION).(string); !ok || v == "" {
		t.Errorf("cssselect.VERSION should be string, got: %#v", cssselect.VERSION)
	}
	if cssselect.VERSION != cssselect.__version__ {
		t.Errorf("cssselect.VERSION(%v) != cssselect.__version__(%v)", cssselect.VERSION, cssselect.__version__)
	}
}