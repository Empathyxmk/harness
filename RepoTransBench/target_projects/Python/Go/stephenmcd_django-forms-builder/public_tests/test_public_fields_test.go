package public_tests

import (
	"testing"
	"stephenmcd_django_forms_builder/formsbuilder"
)

func TestPublicFieldToPythonBooleanTrue(t *testing.T) {
	booleanField := formsbuilder.FIELD_MAP["boolean"]()
	res := booleanField.ToPython("on")
	if res != true {
		t.Errorf("expected boolean 'on' to give true, got %v", res)
	}
}

func TestPublicFieldToPythonBooleanFalse(t *testing.T) {
	booleanField := formsbuilder.FIELD_MAP["boolean"]()
	res1 := booleanField.ToPython("")
	if res1 != false {
		t.Errorf("expected '' to return false, got %v", res1)
	}
	res2 := booleanField.ToPython(nil)
	if res2 != false {
		t.Errorf("expected nil to return false, got %v", res2)
	}
}

func TestPublicFieldToPythonSelect(t *testing.T) {
	selectField := formsbuilder.FIELD_MAP["select"]("orange|banana|pear")
	choices := selectField.GetChoices()
	expected := []string{"orange", "banana", "pear"}
	if len(choices) != 3 || choices[0] != "orange" || choices[1] != "banana" || choices[2] != "pear" {
		t.Errorf("expected %v, got %v", expected, choices)
	}
}

func TestPublicPrettyNameWithNumber(t *testing.T) {
	got := formsbuilder.PrettyName("item_123_value")
	exp := "Item 123 value"
	if got != exp {
		t.Errorf("expected '%s', got '%s'", exp, got)
	}
}