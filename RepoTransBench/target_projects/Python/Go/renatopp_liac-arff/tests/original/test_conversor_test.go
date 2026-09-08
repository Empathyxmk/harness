package original

import (
	"fmt"
	"reflect"
	"strings"
	"testing"
)

// We'll need arff.go to have implemented the required ARFF reader, loader, etc.
import "renatopp_liac-arff/arff"

// Helper types for error emulation, to match Python's custom error classes
type BadNominalValue struct{ msg string }
func (e BadNominalValue) Error() string   { return e.msg }

type BadNumericalValue struct{ msg string }
func (e BadNumericalValue) Error() string { return e.msg }

// Utility: compare for nil used as equivalent to Python's None
func isNil(i any) bool {
	return i == nil || reflect.ValueOf(i).IsNil()
}

// Helper: Simulate the Python assertRaises (for errors)
func assertRaises(t *testing.T, expectedType interface{}, f func()) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Exception of type %T was expected but nothing was raised", expectedType)
		} else {
			if expected, ok := expectedType.(error); ok {
				if gotErr, ok := r.(error); ok {
					expectedName := reflect.TypeOf(expected).Name()
					gotName := reflect.TypeOf(gotErr).Name()
					if expectedName != gotName {
						t.Fatalf("Expected error type %s but got %s", expectedName, gotName)
					}
				} else {
					t.Fatalf("Expected error but got non-error (type %T): %v", r, r)
				}
			}
		}
	}()
	f()
}

// BaseTestDecodeConversor provides base test logic (no state in Go, share logic via embedding)
type BaseTestDecodeConversor struct {
	UseSparse bool
}

// getTestData creates the equivalent ARFF string
func getArffTestData(returnType, typ string, useSparse bool, values []string) string {
	var arffType string
	encodeNominal := typ == "ENCODED_NOMINAL"
	if len(values) > 0 {
		arffType = "{" + strings.Join(values, ",") + "}"
	} else {
		arffType = typ
	}
	var data string
	if useSparse {
		data = fmt.Sprintf("{ 0 %%s }", "%s")
	} else {
		data = fmt.Sprintf("%%s,0")
	}
	template := `
@RELATION testing

@ATTRIBUTE name %s
@ATTRIBUTE dummy REAL

@DATA
%s
`
	sampleData := ""
	returnTypeStr := ""
	switch returnType {
	case "dense":
		returnTypeStr = ""
	default:
		returnTypeStr = "" // placeholder if decoding modes are needed
	}
	sampleData = fmt.Sprintf(template, arffType, data)
	return sampleData + returnTypeStr
}

// The "conversor" returned in tests: a closure that loads an ARFF string with the specified value and returns the parsed value.
func (b *BaseTestDecodeConversor) getConversor(returnType, typ string, values []string) func(string) any {
	return func(val string) any {
		arffTxt := getArffTestData(returnType, typ, b.UseSparse, values)
		var data string
		if b.UseSparse {
			data = fmt.Sprintf("{ 0 %s }", val)
		} else {
			data = fmt.Sprintf("%s,0", val)
		}
		// Replace placeholder with our test value
		arffTxtLines := strings.Split(arffTxt, "\n")
		for i, line := range arffTxtLines {
			if strings.HasPrefix(line, "@DATA") && i+1 < len(arffTxtLines) {
				arffTxtLines[i+1] = data
			}
		}
		arffInput := strings.Join(arffTxtLines, "\n")
		// This function must call the actual ARFF loader from arff.go and extract the value from the first row, first column.
		// Use arff.Load for the interface
		parsed, err := arff.Load(strings.NewReader(arffInput))
		if err != nil {
			panic(err) // Will be caught as error by assertRaises.
		}
		// Extracts the [0][0] value
		if len(parsed.Data) == 0 || len(parsed.Data[0]) == 0 {
			panic(fmt.Errorf("No data returned by arff loader"))
		}
		return parsed.Data[0][0]
	}
}

// ---------- DENSE TESTS ----------

type TestDecodeConversorDense struct {
	BaseTestDecodeConversor
}

func newTestDecodeConversorDense() *TestDecodeConversorDense {
	return &TestDecodeConversorDense{BaseTestDecodeConversor{UseSparse: false}}
}

func TestDecodeConversorDense_Real(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "REAL", nil)

	// Integer to float
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

	// Float to float
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

func TestDecodeConversorDense_Numeric(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "NUMERIC", nil)

	// Integer to float
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

	// Float to float
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

func TestDecodeConversorDense_Integer(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "INTEGER", nil)

	// Integer to integer
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

	// Float as string to integer
	fixture = "\"45.13233322\""
	result = conversor(fixture)
	expected = 45 // Should match truncation as per ARFF loader
	switch val := result.(type) {
	case int:
		if val != expected {
			t.Errorf("Expected %v, got %v", expected, val)
		}
	default:
		t.Errorf("Type mismatch: expected int but got %T", result)
	}
}

func TestDecodeConversorDense_String(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "STRING", nil)

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

func TestDecodeConversorDense_Nominal(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "NOMINAL", []string{"a", "b", "3.4"})

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

func TestDecodeConversorDense_EncodedNominal(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "ENCODED_NOMINAL", []string{"a", "b", "3.4"})
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

func TestDecodeConversorDense_NullValue(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "NOMINAL", []string{"a", "b", "3.4"})
	result := conversor("?")
	if result != nil {
		t.Errorf("Expected nil (None), got %v", result)
	}

	// Only test empty string for dense
	result = conversor("")
	if result != nil {
		t.Errorf("Expected nil (None) for empty string, got %v", result)
	}

	conversor = c.getConversor("dense", "ENCODED_NOMINAL", []string{"a", "b", "3.4"})
	result = conversor("?")
	if result != nil {
		t.Errorf("Expected nil (None), got %v", result)
	}

	result = conversor("")
	if result != nil {
		t.Errorf("Expected nil (None) for empty string, got %v", result)
	}

	conversor = c.getConversor("dense", "INTEGER", nil)
	result = conversor("?")
	if result != nil {
		t.Errorf("Expected nil (None), got %v", result)
	}
	result = conversor("")
	if result != nil {
		t.Errorf("Expected nil (None) for empty string, got %v", result)
	}
}

func TestDecodeConversorDense_PaddingValue(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "NUMERIC", nil)

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

func TestDecodeConversorDense_InvalidNominalValue(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "NOMINAL", []string{"a", "b", "3.4"})
	assertRaises(t, BadNominalValue{""}, func() {
		conversor("ABACATE")
	})
}

func TestDecodeConversorDense_InvalidNumericalValue(t *testing.T) {
	c := newTestDecodeConversorDense()
	conversor := c.getConversor("dense", "REAL", nil)
	assertRaises(t, BadNumericalValue{""}, func() {
		conversor("ABACATE")
	})

	conversor = c.getConversor("dense", "NUMERIC", nil)
	assertRaises(t, BadNumericalValue{""}, func() {
		conversor("ABACATE")
	})

	conversor = c.getConversor("dense", "INTEGER", nil)
	assertRaises(t, BadNumericalValue{""}, func() {
		conversor("ABACATE")
	})
}