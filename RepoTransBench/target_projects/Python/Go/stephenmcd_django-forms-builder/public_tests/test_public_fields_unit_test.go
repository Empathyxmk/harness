package public_tests

import (
	"testing"
	"stephenmcd_django_forms_builder/formsbuilder"
)

func TestPublicSplitChoicesDiffInput(t *testing.T) {
	value := "red|green|blue"
	out := formsbuilder.SplitChoices(value, "|")
	sl, ok := out.([]string)
	if !ok {
		t.Fatalf("expected []string, got %T", out)
	}
	exp := []string{"red", "green", "blue"}
	if len(sl) != 3 || sl[0] != "red" || sl[1] != "green" || sl[2] != "blue" {
		t.Errorf("expected %v, got %v", exp, sl)
	}
}

func TestPublicPrettyNameDiffInput(t *testing.T) {
	got := formsbuilder.PrettyName("zip_code")
	exp := "Zip code"
	if got != exp {
		t.Errorf("expected '%s', got '%s'", exp, got)
	}
}

func TestPublicIsEmptyDiffInput(t *testing.T) {
	if !formsbuilder.IsEmpty(nil) {
		t.Error("IsEmpty should be true for nil")
	}
	if formsbuilder.IsEmpty([]string{"value"}) {
		t.Error("IsEmpty should be false for non-empty list")
	}
	if !formsbuilder.IsEmpty("      ") {
		t.Error("IsEmpty should be true for whitespace-only string")
	}
}