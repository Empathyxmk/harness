package public_tests

import (
	"reflect"
	"testing"
	"eatonphil_pj/pj"
)

func TestObjectMultipleKeys(t *testing.T) {
	got := pj.FromString(`{"alpha":42, "beta":"xyz"}`)
	want := map[string]interface{}{"alpha": 42, "beta": "xyz"}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestObjectArrayNumbers(t *testing.T) {
	got := pj.FromString(`{"nums":[7,8,9]}`)
	want := map[string]interface{}{"nums": []interface{}{7, 8, 9}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestObjectBoolean(t *testing.T) {
	got := pj.FromString(`{"success":false}`)
	want := map[string]interface{}{"success": false}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestObjectWithNull(t *testing.T) {
	got := pj.FromString(`{"unset":null}`)
	want := map[string]interface{}{"unset": nil}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestObjectWithFloat(t *testing.T) {
	got := pj.FromString(`{"value":2.718}`)
	want := map[string]interface{}{"value": 2.718}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestNestedArray(t *testing.T) {
	got := pj.FromString(`{"arr":[[1,2],[],[3]]}`)
	want := map[string]interface{}{
		"arr": []interface{}{
			[]interface{}{1, 2},
			[]interface{}{},
			[]interface{}{3},
		},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestNestedObjectMultipleLevels(t *testing.T) {
	got := pj.FromString(`{"outer":{"inner":{"leaf":10}}}`)
	want := map[string]interface{}{
		"outer": map[string]interface{}{
			"inner": map[string]interface{}{
				"leaf": 10,
			},
		},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestArrayOfObjects(t *testing.T) {
	got := pj.FromString(`{"users":[{"id":1},{"id":2}]}`)
	want := map[string]interface{}{
		"users": []interface{}{
			map[string]interface{}{"id": 1},
			map[string]interface{}{"id": 2},
		},
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestBasicStringWithWhitespace(t *testing.T) {
	got := pj.FromString(`{   "k"    :   "v"   }`)
	want := map[string]interface{}{"k": "v"}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}

func TestZeroInt(t *testing.T) {
	got := pj.FromString(`{"z":0}`)
	want := map[string]interface{}{"z": 0}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("expected %v, got %v", want, got)
	}
}