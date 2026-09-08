package original

import (
	"reflect"
	"testing"

	"stephenmcd_django_forms_builder/formsbuilder"
)

func TestSplitChoicesString(t *testing.T) {
	s := "Red\nBlue\r\nGreen"
	got := formsbuilder.SplitChoices(s)
	exp := []string{"Red", "Blue", "Green"}
	if !reflect.DeepEqual(got, exp) {
		t.Errorf("expected %v, got %v", exp, got)
	}
}

func TestSplitChoicesEmpty(t *testing.T) {
	got := formsbuilder.SplitChoices("")
	if l := len(got.([]string)); l != 0 {
		t.Errorf("expected empty list, got len=%d", l)
	}
	got = formsbuilder.SplitChoices(nil)
	if l := len(got.([]string)); l != 0 {
		t.Errorf("expected empty list for nil, got len=%d", l)
	}
	got = formsbuilder.SplitChoices(0)
	if l := len(got.([]string)); l != 0 {
		t.Errorf("expected empty list for 0, got len=%d", l)
	}
	got = formsbuilder.SplitChoices(3.14)
	if l := len(got.([]string)); l != 0 {
		t.Errorf("expected empty list for 3.14, got len=%d", l)
	}
}

func TestSplitChoicesListOfTuples(t *testing.T) {
	lst := [][2]string{{"A", "Apple"}, {"B", "Banana"}}
	got := formsbuilder.SplitChoices(lst)
	if !reflect.DeepEqual(got, lst) {
		t.Errorf("expected pass-through %v, got %v", lst, got)
	}
}

func TestSplitChoicesTupleOfTuples(t *testing.T) {
	// Go has only slices; test same.
	tpl := [][2]string{{"A", "Apple"}, {"B", "Banana"}}
	got := formsbuilder.SplitChoices(tpl)
	if !reflect.DeepEqual(got, tpl) {
		t.Errorf("expected %v, got %v", tpl, got)
	}
}

func TestSplitChoicesLeadingTrailingWhitespace(t *testing.T) {
	s := " Red \n\n Blue"
	got := formsbuilder.SplitChoices(s)
	exp := []string{"Red", "Blue"}
	if !reflect.DeepEqual(got, exp) {
		t.Errorf("expected %v, got %v", exp, got)
	}
}

func TestAliasChoicesFromLines(t *testing.T) {
	s := "One\nTwo"
	res := formsbuilder.ChoicesFromLines(s)
	exp := [][2]string{{"One", "One"}, {"Two", "Two"}}
	if !reflect.DeepEqual(res, exp) {
		t.Errorf("expected %v, got %v", exp, res)
	}
}

func TestFieldChoicesAndTypes(t *testing.T) {
	if reflect.TypeOf(formsbuilder.FIELD_CHOICES).Kind() != reflect.Slice {
		t.Errorf("FIELD_CHOICES should be a slice")
	}
	if reflect.TypeOf(formsbuilder.FIELD_TYPES).Kind() != reflect.Slice {
		t.Errorf("FIELD_TYPES should be a slice")
	}
	for _, i := range formsbuilder.FIELD_TYPES {
		if reflect.TypeOf(i).Kind() != reflect.Array && reflect.TypeOf(i).Kind() != reflect.Slice {
			t.Errorf("FIELD_TYPES inner should be tuple/array, got %v", reflect.TypeOf(i))
		}
	}
	typesFromChoices := make([][2]string, len(formsbuilder.FIELD_CHOICES))
	for idx, kv := range formsbuilder.FIELD_CHOICES {
		typesFromChoices[idx] = [2]string{kv[0], kv[1]}
	}
	if !reflect.DeepEqual(formsbuilder.FIELD_TYPES, typesFromChoices) {
		t.Errorf("FIELD_TYPES should equal tuple(field_choices...)")
	}
}