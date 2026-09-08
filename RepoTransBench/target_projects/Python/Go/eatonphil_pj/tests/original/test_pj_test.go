package original

import (
	"reflect"
	"testing"
	"eatonphil_pj/pj"
)

func TestEmptyObject(t *testing.T) {
	got := pj.FromString(`{}`)
	want := map[string]interface{}{}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestBasicObject(t *testing.T) {
	got := pj.FromString(`{"foo":"bar"}`)
	want := map[string]interface{}{"foo": "bar"}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestBasicNumber(t *testing.T) {
	got := pj.FromString(`{"foo":1}`)
	want := map[string]interface{}{"foo": 1}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestEmptyArray(t *testing.T) {
	got := pj.FromString(`{"foo":[]}`)
	want := map[string]interface{}{"foo": []interface{}{}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestBasicArray(t *testing.T) {
	got := pj.FromString(`{"foo":[1,2,"three"]}`)
	want := map[string]interface{}{
		"foo": []interface{}{1, 2, "three"},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestNestedObject(t *testing.T) {
	got := pj.FromString(`{"foo":{"bar":2}}`)
	want := map[string]interface{}{
		"foo": map[string]interface{}{"bar": 2},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestTrueValue(t *testing.T) {
	got := pj.FromString(`{"foo":true}`)
	want := map[string]interface{}{"foo": true}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestFalseValue(t *testing.T) {
	got := pj.FromString(`{"foo":false}`)
	want := map[string]interface{}{"foo": false}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestNullValue(t *testing.T) {
	got := pj.FromString(`{"foo":null}`)
	want := map[string]interface{}{"foo": nil}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestBasicWhitespace(t *testing.T) {
	got := pj.FromString(`{ "foo" : [1, 2, "three"] }`)
	want := map[string]interface{}{
		"foo": []interface{}{1, 2, "three"},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}