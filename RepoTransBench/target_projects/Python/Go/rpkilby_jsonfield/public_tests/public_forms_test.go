package public_tests

import (
	"reflect"
	"testing"
	"rpkilby_jsonfield/src/jsonfield"
)

type DummyFormStruct struct {
	Payload interface{}
}

func TestBlankForm(t *testing.T) {
	field := jsonfield.NewJSONFormField(false)
	val, err := field.Clean("")
	if err != nil || val != nil {
		t.Errorf("Blank form failed: err=%v val=%v", err, val)
	}
}

func TestValidJSONFormValue(t *testing.T) {
	field := jsonfield.NewJSONFormField(false)
	val, err := field.Clean(`{"species": "cat", "legs": 4}`)
	if err != nil {
		t.Fatalf("Unexpected error for valid JSON: %v", err)
	}
	m, ok := val.(map[string]interface{})
	if !ok || m["species"] != "cat" || m["legs"] != float64(4) {
		t.Errorf("Wrong value: %v", val)
	}
}

func TestInvalidJSONFormValue(t *testing.T) {
	field := jsonfield.NewJSONFormField(false)
	_, err := field.Clean(`{"species": unquoted}`)
	if err == nil {
		t.Error("Expected error for invalid input")
	}
}

func TestPythonObjInput(t *testing.T) {
	field := jsonfield.NewJSONFormField(false)
	in := map[string]interface{}{"key": []interface{}{float64(1), float64(2)}}
	val, err := field.Clean(in)
	if err != nil {
		t.Errorf("Python obj clean failed: %v", err)
	}
	if !reflect.DeepEqual(val, in) {
		t.Errorf("Expected value to roundtrip: %v", val)
	}
}