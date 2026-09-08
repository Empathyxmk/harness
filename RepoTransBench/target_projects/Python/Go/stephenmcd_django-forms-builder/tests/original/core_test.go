package original

import (
	"reflect"
	"testing"

	"stephenmcd_django_forms_builder/formsbuilder"
)

func TestFieldChoicesDict(t *testing.T) {
	choices := "Red\nGreen\nBlue"
	expected := [][2]string{{"Red", "Red"}, {"Green", "Green"}, {"Blue", "Blue"}}
	got := formsbuilder.ChoicesFromLines(choices)
	if !reflect.DeepEqual(got, expected) {
		t.Errorf("expected %v, got %v", expected, got)
	}
}

func TestFieldChoicesDictEmpty(t *testing.T) {
	v := formsbuilder.ChoicesFromLines("")
	if l := len(v); l != 0 {
		t.Errorf("expected empty result, got %v", v)
	}
}

func TestIsFile(t *testing.T) {
	if !formsbuilder.IsFile("photo.PNG") {
		t.Error("Expected photo.PNG to be recognized as file")
	}
	if !formsbuilder.IsFile("document.PDF") {
		t.Error("Expected document.PDF to be recognized as file")
	}
	if formsbuilder.IsFile("example.txt") {
		t.Error("example.txt should NOT be recognized as file")
	}
	if formsbuilder.IsFile("no_dot") {
		t.Error("no_dot should NOT be recognized as file")
	}
}

func TestSlugifyStripAndLower(t *testing.T) {
	s := " Hello__World__ "
	sl := formsbuilder.Slugify(s)
	if sl != "hello-world" {
		t.Errorf("expected slugify to 'hello-world', got %s", sl)
	}
}

func TestSettingImports(t *testing.T) {
	if _, ok := interface{}(formsbuilder.USE_SITES).(bool); !ok {
		t.Error("USE_SITES should be bool")
	}
	if _, ok := interface{}(formsbuilder.USE_THREADED_EMAILS).(bool); !ok {
		t.Error("USE_THREADED_EMAILS should be bool")
	}
	if _, ok := interface{}(formsbuilder.EXTRA_FIELD_TYPES).([]string); !ok {
		t.Error("EXTRA_FIELD_TYPES should be a string slice")
	}
}