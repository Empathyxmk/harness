package original

import (
	"fmt"
	"reflect"
	"strings"
	"testing"

	"renatopp_liac-arff/arff"
)

type TestDecodeConversorSparse struct {
	BaseTestDecodeConversor
}

func newTestDecodeConversorSparse() *TestDecodeConversorSparse {
	return &TestDecodeConversorSparse{BaseTestDecodeConversor{UseSparse: true}}
}

func TestDecodeConversorSparse_Real(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "REAL", nil)

	fixture := "45"
	result := conversor(fixture)
	expected := 45.0
	switch val := result.(type) {
	case float64:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected float64 but got %T", result)
	}

	fixture = "45.13233322"
	result = conversor(fixture)
	expected = 45.13233322
	switch val := result.(type) {
	case float64:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected float64 but got %T", result)
	}
}

func TestDecodeConversorSparse_Numeric(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "NUMERIC", nil)

	fixture := "45"
	result := conversor(fixture)
	expected := 45.0
	switch val := result.(type) {
	case float64:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected float64 but got %T", result)
	}

	fixture = "45.13233322"
	result = conversor(fixture)
	expected = 45.13233322
	switch val := result.(type) {
	case float64:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected float64 but got %T", result)
	}
}

func TestDecodeConversorSparse_Integer(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "INTEGER", nil)

	fixture := "45"
	result := conversor(fixture)
	expected := 45
	switch val := result.(type) {
	case int:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected int but got %T", result)
	}

	fixture = "\"45.13233322\""
	result = conversor(fixture)
	expected = 45
	switch val := result.(type) {
	case int:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected int but got %T", result)
	}
}

func TestDecodeConversorSparse_String(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "STRING", nil)

	fixture := "raposa"
	result := conversor(fixture)
	expected := "raposa"
	if result != expected {
		t.Errorf("Expected %v, got %v", expected, result)
	}

	fixture = "\"raposa\""
	result = conversor(fixture)
	expected = "raposa"
	if result != expected {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

func TestDecodeConversorSparse_Nominal(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "NOMINAL", []string{"a", "b", "3.4"})

	fixture := "a"
	expected := "a"
	if result := conversor(fixture); result != expected {
		t.Errorf("Expected %v, got %v", expected, result)
	}
	fixture = "3.4"
	expected = "3.4"
	if result := conversor(fixture); result != expected {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

func TestDecodeConversorSparse_EncodedNominal(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "ENCODED_NOMINAL", []string{"a", "b", "3.4"})
	tests := []struct {
		fixture  string
		expected int
	}{
		{"a", 0},
		{"b", 1},
		{"3.4", 2},
	}
	for _, test := range tests {
		result := conversor(test.fixture)
		if result != test.expected {
			t.Errorf("Expected %v, got %v for input %v", test.expected, result, test.fixture)
		}
	}
}

func TestDecodeConversorSparse_NullValue(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "NOMINAL", []string{"a", "b", "3.4"})
	result := conversor("?")
	if result != nil {
		t.Errorf("Expected nil (None), got %v", result)
	}
	// Empty string is not tested for sparse

	conversor = c.getConversor("sparse", "ENCODED_NOMINAL", []string{"a", "b", "3.4"})
	result = conversor("?")
	if result != nil {
		t.Errorf("Expected nil (None), got %v", result)
	}
	// Empty string is not tested for sparse

	conversor = c.getConversor("sparse", "INTEGER", nil)
	result = conversor("?")
	if result != nil {
		t.Errorf("Expected nil (None), got %v", result)
	}
	// Empty string is not tested for sparse
}

func TestDecodeConversorSparse_PaddingValue(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "NUMERIC", nil)

	fixture := "      45     "
	result := conversor(fixture)
	expected := 45.0
	switch val := result.(type) {
	case float64:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected float64 but got %T", result)
	}
}

func TestDecodeConversorSparse_InvalidNominalValue(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "NOMINAL", []string{"a", "b", "3.4"})
	assertRaises(t, BadNominalValue{""}, func() {
		conversor("ABACATE")
	})
}

func TestDecodeConversorSparse_InvalidNumericalValue(t *testing.T) {
	c := newTestDecodeConversorSparse()
	conversor := c.getConversor("sparse", "REAL", nil)
	assertRaises(t, BadNumericalValue{""}, func() {
		conversor("ABACATE")
	})

	conversor = c.getConversor("sparse", "NUMERIC", nil)
	assertRaises(t, BadNumericalValue{""}, func() {
		conversor("ABACATE")
	})

	conversor = c.getConversor("sparse", "INTEGER", nil)
	assertRaises(t, BadNumericalValue{""}, func() {
		conversor("ABACATE")
	})
}