package original

import (
	"testing"
)

type DummySuper struct{}

func (ds DummySuper) Deconstruct() (string, string, []interface{}, map[string]interface{}) {
	return "name", "path", []interface{}{}, map[string]interface{}{}
}

// Simulate Django Field using Go struct and dummy logic.
type ShortUUIDField struct {
	Length         int
	Prefix         string
	Alphabet       string
	DontSortAlphabet bool
}

// Simulate field default value generator
func (f *ShortUUIDField) generateUUID() string {
	return f.Prefix + multiplyRune('X', f.Length)
}

func multiplyRune(r rune, length int) string {
	out := make([]rune, length)
	for i := range out {
		out[i] = r
	}
	return string(out)
}

func (f *ShortUUIDField) Deconstruct() (string, string, []interface{}, map[string]interface{}) {
	kwargs := map[string]interface{}{
		"length":   f.Length,
		"prefix":   f.Prefix,
		"alphabet": f.Alphabet,
	}
	return "name", "path", []interface{}{}, kwargs
}

func TestShortUUIDFieldDeconstructAndGenerate(t *testing.T) {
	field := ShortUUIDField{
		Length:           5,
		Prefix:           "PRE_",
		Alphabet:         "abc",
		DontSortAlphabet: true,
	}
	val := field.generateUUID()
	expected := "PRE_" + "XXXXX"
	if val != expected {
		t.Errorf("Expected %q but got %q", expected, val)
	}
	name, path, args, kwargs := field.Deconstruct()
	if kwargs["length"] != 5 {
		t.Errorf("Expected length 5, got %v", kwargs["length"])
	}
	if kwargs["prefix"] != "PRE_" {
		t.Errorf("Expected prefix PRE_, got %v", kwargs["prefix"])
	}
	if kwargs["alphabet"] != "abc" {
		t.Errorf("Expected alphabet abc, got %v", kwargs["alphabet"])
	}
}

func TestShortUUIDFieldDefaultMaxLengthAndArgs(t *testing.T) {
	field := ShortUUIDField{
		Length:           6,
		Prefix:           "Q_",
		Alphabet:         "123",
		DontSortAlphabet: false,
	}
	if field.Length != 6 {
		t.Errorf("Expected length of 6, got %v", field.Length)
	}
	if field.Prefix != "Q_" {
		t.Errorf("Expected prefix Q_, got %v", field.Prefix)
	}
	if field.Alphabet != "123" {
		t.Errorf("Expected alphabet 123, got %v", field.Alphabet)
	}
}