package original

import (
	"strings"
	"testing"

	"stephenmcd_django_forms_builder/formsbuilder"
)

func TestVersionString(t *testing.T) {
	v := formsbuilder.Version
	if !strings.Contains(v, ".") {
		t.Errorf("version should be string with dots, got %v", v)
	}
	splits := strings.Count(v, ".")
	if splits != 2 {
		t.Errorf("version should have 2 dots (3 parts), got %d", splits)
	}
}