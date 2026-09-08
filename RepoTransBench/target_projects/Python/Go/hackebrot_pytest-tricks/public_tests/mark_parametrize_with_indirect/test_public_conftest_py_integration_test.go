package public_tests

import (
	"testing"
	"reflect"
)

func TestConftestPyRecipe(t *testing.T) {
	recipes := map[string][]string{
		"spicytuna": {"tuna", "sriracha", "scallions"},
		"rainbow":   {"tuna", "avocado", "shrimp", "salmon"},
	}
	for sushi, expected := range recipes {
		got := recipes[sushi]
		if !reflect.DeepEqual(got, expected) {
			t.Errorf("%s expected %v, got %v", sushi, expected, got)
		}
	}
}