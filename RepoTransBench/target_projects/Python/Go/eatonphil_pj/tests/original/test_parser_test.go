package original

import (
	"testing"
	"eatonphil_pj/pj/parser"
	"reflect"
)

func TestParseArrayEmpty(t *testing.T) {
	val, tokens, err := parser.ParseArray([]interface{}{"]"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{}
	if !reflect.DeepEqual(val, want) {
		t.Errorf("expected %v, got %v", want, val)
	}
	if len(tokens) != 0 {
		t.Errorf("expected empty tokens, got %v", tokens)
	}
}

func TestParseArrayMultiple(t *testing.T) {
	toks := []interface{}{1, ",", 2, "]", "leftover"}
	arr, rest, err := parser.ParseArray(toks)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{1, 2}
	if !reflect.DeepEqual(arr, want) {
		t.Errorf("expected %v, got %v", want, arr)
	}
	wantRest := []interface{}{"leftover"}
	if !reflect.DeepEqual(rest, wantRest) {
		t.Errorf("expected %v, got %v", wantRest, rest)
	}
}

func TestParseArrayError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic (error case), got none")
		}
	}()
	_, _, _ = parser.ParseArray([]interface{}{1, 2, "]"})
}

func TestParseObjectEmpty(t *testing.T) {
	val, tokens, err := parser.ParseObject([]interface{}{"}"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := map[string]interface{}{}
	if !reflect.DeepEqual(val, want) {
		t.Errorf("expected %v, got %v", want, val)
	}
	if len(tokens) != 0 {
		t.Errorf("expected empty tokens, got %v", tokens)
	}
}

func TestParseObjectBasic(t *testing.T) {
	toks := []interface{}{"key", ":", 42, "}"}
	obj, rest, err := parser.ParseObject(toks)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := map[string]interface{}{"key": 42}
	if !reflect.DeepEqual(obj, want) {
		t.Errorf("expected %v, got %v", want, obj)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseObjectMultiple(t *testing.T) {
	toks := []interface{}{"a", ":", 1, ",", "b", ":", 2, "}", "end"}
	obj, rest, err := parser.ParseObject(toks)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := map[string]interface{}{"a": 1, "b": 2}
	if !reflect.DeepEqual(obj, want) {
		t.Errorf("expected %v, got %v", want, obj)
	}
	wantRest := []interface{}{"end"}
	if !reflect.DeepEqual(rest, wantRest) {
		t.Errorf("expected %v, got %v", wantRest, rest)
	}
}

func TestParseObjectKeyNonString(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic (non-string key), got none")
		}
	}()
	_, _, _ = parser.ParseObject([]interface{}{1, ":", 2, "}"})
}

func TestParseObjectColonMissing(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic (missing colon), got none")
		}
	}()
	_, _, _ = parser.ParseObject([]interface{}{"key", 42, "}"})
}

func TestParseObjectCommaMissing(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic (missing comma), got none")
		}
	}()
	_, _, _ = parser.ParseObject([]interface{}{"key", ":", 1, 42, "}"})
}

func TestParseArrayMissingEnd(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic (missing end), got none")
		}
	}()
	_, _, _ = parser.ParseArray([]interface{}{1, ","})
}

func TestParseObjectMissingEnd(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic (missing end), got none")
		}
	}()
	_, _, _ = parser.ParseObject([]interface{}{"key", ":", 1})
}

func TestParseRootNonObject(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic (non-object root), got none")
		}
	}()
	_, _ = parser.Parse([]interface{}{"[", 1, "]"}, true)
}

func TestParseArrayDelegation(t *testing.T) {
	arr, rest, err := parser.Parse([]interface{}{"[", 1, ",", 2, "]"}, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := []interface{}{1, 2}
	if !reflect.DeepEqual(arr, want) {
		t.Errorf("expected %v, got %v", want, arr)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseObjectDelegation(t *testing.T) {
	obj, rest, err := parser.Parse([]interface{}{"{", "a", ":", 3, "}"}, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := map[string]interface{}{"a": 3}
	if !reflect.DeepEqual(obj, want) {
		t.Errorf("expected %v, got %v", want, obj)
	}
	if len(rest) != 0 {
		t.Errorf("expected empty rest, got %v", rest)
	}
}

func TestParseLiteral(t *testing.T) {
	val, rest, err := parser.Parse([]interface{}{42, ",", 100}, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if val != 42 {
		t.Errorf("expected 42, got %v", val)
	}
	wantRest := []interface{}{",", 100}
	if !reflect.DeepEqual(rest, wantRest) {
		t.Errorf("expected %v, got %v", wantRest, rest)
	}
}