package public_tests

import (
	"reflect"
	"testing"
	"eatonphil_pj/pj/parser"
)

func TestParseEmptyList(t *testing.T) {
	tokens := []interface{}{"[", "]"}
	value, rest, err := parser.Parse(tokens, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{}
	if !reflect.DeepEqual(value, want) {
		t.Errorf("expected %v, got %v", want, value)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseIntArray(t *testing.T) {
	tokens := []interface{}{"[", 99, ",", 88, "]"}
	value, rest, err := parser.Parse(tokens, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{99, 88}
	if !reflect.DeepEqual(value, want) {
		t.Errorf("expected %v, got %v", want, value)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseFloatAndNull(t *testing.T) {
	tokens := []interface{}{"[", 1.5, ",", nil, "]"}
	value, rest, err := parser.Parse(tokens, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{1.5, nil}
	if !reflect.DeepEqual(value, want) {
		t.Errorf("expected %v, got %v", want, value)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseObjectWithArray(t *testing.T) {
	tokens := []interface{}{"{", "items", ":", "[", 2, ",", 3, "]", "}"}
	value, rest, err := parser.Parse(tokens, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := map[string]interface{}{"items": []interface{}{2, 3}}
	if !reflect.DeepEqual(value, want) {
		t.Errorf("expected %v, got %v", want, value)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseObjectWithNestedObj(t *testing.T) {
	tokens := []interface{}{"{", "a", ":", "{", "b", ":", 1, "}", "}"}
	value, rest, err := parser.Parse(tokens, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := map[string]interface{}{
		"a": map[string]interface{}{"b": 1},
	}
	if !reflect.DeepEqual(value, want) {
		t.Errorf("expected %v, got %v", want, value)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseBools(t *testing.T) {
	tokens := []interface{}{"[", true, ",", false, "]"}
	value, rest, err := parser.Parse(tokens, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{true, false}
	if !reflect.DeepEqual(value, want) {
		t.Errorf("expected %v, got %v", want, value)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseStringAndWhitespace(t *testing.T) {
	tokens := []interface{}{"[", "hi", ",", "world", "]"}
	value, rest, err := parser.Parse(tokens, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{"hi", "world"}
	if !reflect.DeepEqual(value, want) {
		t.Errorf("expected %v, got %v", want, value)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}