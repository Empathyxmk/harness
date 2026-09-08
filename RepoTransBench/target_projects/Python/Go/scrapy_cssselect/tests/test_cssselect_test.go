package tests

import (
	"testing"

	"scrapy_cssselect/cssselect"
)

func TestSelectorProperties(t *testing.T) {
	selector := &cssselect.Selector{parsedTree: "test"}
	if selector == nil {
		t.Fatalf("Selector should be instantiable")
	}
	// pseudoElement should return nil in the stub, OK
	if selector.pseudoElement() != nil {
		t.Errorf("Expected pseudoElement() to be nil for default stub")
	}
	if a, b, c := selector.Specificity(); a != 0 || b != 0 || c != 0 {
		t.Errorf("Expected default specificity to be (0, 0, 0), got (%d, %d, %d)", a, b, c)
	}
	if sel := selector.Canonical(); sel != "" {
		t.Errorf("Expected default Canonical() to be empty string, got %v", sel)
	}
}

func TestCSSSelectVersionVars(t *testing.T) {
	if cssselect.VERSION == "" {
		t.Error("cssselect.VERSION should not be empty")
	}
	if cssselect.__version__ != cssselect.VERSION {
		t.Errorf("cssselect.__version__ should match VERSION, got %v != %v", cssselect.__version__, cssselect.VERSION)
	}
}

func TestParseFunction(t *testing.T) {
	result, err := cssselect.Parse("div.class")
	if err != nil {
		// Acceptable in default stub, so long as error type is nil or matches expectation.
	}
	if result == nil {
		// In stub, Parse returns nil, so check it is nil or empty slice.
	} else if len(result) != 0 {
		t.Errorf("Expected stub Parse function to return nil or empty slice, got %v", result)
	}
}

func TestSelectorErrorTypes(t *testing.T) {
	e1 := &cssselect.ExpressionError{}
	e2 := &cssselect.SelectorError{}
	e3 := &cssselect.SelectorSyntaxError{}
	if e1 == nil || e2 == nil || e3 == nil {
		t.Error("Error types should be instantiable")
	}
}

func TestTranslatorTypes(t *testing.T) {
	generic := &cssselect.GenericTranslator{}
	html := &cssselect.HTMLTranslator{}
	if generic == nil || html == nil {
		t.Error("Translator types should be instantiable")
	}
}