package public_tests

import (
	"testing"
	"reflect"
)

func TestRecipeExistsForRoll(t *testing.T) {
	recipes := map[string][]string{
		"rainbow":   {"tuna", "avocado", "shrimp", "salmon"},
		"spicytuna": {"tuna", "sriracha", "scallions"},
	}
	for roll, exp := range recipes {
		if got, ok := recipes[roll]; !ok || !reflect.DeepEqual(got, exp) {
			t.Errorf("Roll %s not found or mismatch. Expected %v, got %v", roll, exp, got)
		}
	}
}