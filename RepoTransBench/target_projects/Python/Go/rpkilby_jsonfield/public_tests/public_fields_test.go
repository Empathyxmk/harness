package public_tests

import (
	"reflect"
	"testing"
	"rpkilby_jsonfield/src/jsonfield"
)

func TestDeconstructNonDefaultKwargs(t *testing.T) {
	f := jsonfield.NewJSONField(
		jsonfield.WithEncoder("str"),
		jsonfield.WithDecoder("str"),
		jsonfield.WithDumpKwargs(map[string]interface{}{"indent": 4}))
	_, _, _, kwargs := f.Deconstruct()
	if kwargs["encoder_class"] != "str" {
		t.Errorf("encoder_class not set properly")
	}
	if kwargs["decoder_class"] != "str" {
		t.Errorf("decoder_class not set properly")
	}
	if !reflect.DeepEqual(kwargs["dump_kwargs"], map[string]interface{}{"indent": 4}) {
		t.Errorf("dump_kwargs not set properly")
	}
}

func TestDeconstructDefaultKwargs(t *testing.T) {
	f := jsonfield.NewJSONField()
	_, _, _, kwargs := f.Deconstruct()
	if _, ok := kwargs["decoder_class"]; ok {
		t.Error("Should not have decoder_class in kwargs")
	}
	if _, ok := kwargs["encoder_class"]; ok {
		t.Error("Should not have encoder_class in kwargs")
	}
	if _, ok := kwargs["dump_kwargs"]; ok {
		t.Error("Should not have dump_kwargs in kwargs")
	}
}

func TestGetPrepValueCanReturnNoneIfNull(t *testing.T) {
	field := jsonfield.NewJSONField(jsonfield.WithNull(true))
	val := field.GetPrepValue(nil)
	if val != nil {
		t.Errorf("Expected nil, got %v", val)
	}
}

func TestGetPrepValueAlwaysJSONDumpsIfNotNull(t *testing.T) {
	field := jsonfield.NewJSONField(jsonfield.WithNull(true))
	val := field.GetPrepValue(map[string]interface{}{"number": 33, "flag": false})
	if val != `{"number":33,"flag":false}` && val != `{"flag":false,"number":33}` {
		// Map order can vary!
		t.Errorf("Unexpected result for prep value: %v", val)
	}
}

func TestFromDBValueLoadedTypes(t *testing.T) {
	field := jsonfield.NewJSONField()
	got := field.FromDBValue(`{"z":1}`, nil, nil, nil)
	v, ok := got.(map[string]interface{})
	if !ok || v["z"] != float64(1) {
		t.Errorf("Wrong type/val for object: %v", got)
	}
	if field.FromDBValue("", nil, nil, nil) != nil {
		t.Errorf("Empty string should be nil")
	}
}