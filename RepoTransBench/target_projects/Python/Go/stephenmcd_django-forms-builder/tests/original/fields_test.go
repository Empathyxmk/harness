package original

import (
	"reflect"
	"testing"

	"stephenmcd_django_forms_builder/formsbuilder"
)

func TestLinebreakRe(t *testing.T) {
	got := formsbuilder.LinebreakRe().Split("a\nb", -1)
	if !reflect.DeepEqual(got, []string{"a", "b"}) {
		t.Errorf("split on \\n failed: got %v", got)
	}
	got = formsbuilder.LinebreakRe().Split("a\r\nb", -1)
	if !reflect.DeepEqual(got, []string{"a", "b"}) {
		t.Errorf("split on \\r\\n failed: got %v", got)
	}
	got = formsbuilder.LinebreakRe().Split("a\r\nb\nc", -1)
	if !reflect.DeepEqual(got, []string{"a", "b", "c"}) {
		t.Errorf("split on mix failed: got %v", got)
	}
}

func TestFieldTypeIterable(t *testing.T) {
	typesList := formsbuilder.FIELD_TYPES
	if len(typesList) == 0 {
		t.Error("FIELD_TYPES should not be empty")
	}
	for _, tval := range typesList {
		if len(tval) != 2 {
			t.Errorf("type entry should have length 2, got %v", tval)
		}
	}
}

func TestChoicesFromLinesBasic(t *testing.T) {
	choices := "Red\nGreen\nBlue"
	expected := [][2]string{{"Red", "Red"}, {"Green", "Green"}, {"Blue", "Blue"}}
	got := formsbuilder.ChoicesFromLines(choices)
	if !reflect.DeepEqual(got, expected) {
		t.Errorf("expected %v, got %v", expected, got)
	}
}

func TestChoicesFromLinesEmpty(t *testing.T) {
	v := formsbuilder.ChoicesFromLines("")
	if len(v) != 0 {
		t.Errorf("expected empty slice for '', got %v", v)
	}
	v = formsbuilder.ChoicesFromLines(nil)
	if len(v) != 0 {
		t.Errorf("expected empty slice for nil, got %v", v)
	}
	v = formsbuilder.ChoicesFromLines(1)
	if len(v) != 0 {
		t.Errorf("expected empty slice for 1, got %v", v)
	}
	out := formsbuilder.ChoicesFromLines([][2]string{{"foo", "foo"}})
	if !reflect.DeepEqual(out, [][2]string{{"foo", "foo"}}) {
		t.Errorf("expected pass-through list-of-tuples, got %v", out)
	}
}