package original

import (
	"testing"
)

func TestListWithoutHamcrest(t *testing.T) {
	customersNames := []string{"John", "Michael", "Edwin"}
	found := false
	for _, name := range customersNames {
		if name == "John" || name == "Michael" || name == "Edwin" {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected at least one of John, Michael, and Edwin in the list")
	}
}

func TestListWithHamcrest(t *testing.T) {
	customersNames := []string{"John", "Michael", "Edwin"}
	expected := map[string]bool{
		"John":    false,
		"Michael": false,
		"Edwin":   false,
	}
	for _, name := range customersNames {
		if _, ok := expected[name]; ok {
			expected[name] = true
		}
	}
	for name, found := range expected {
		if !found {
			t.Errorf("Expected name %s in customersNames", name)
		}
	}
}