package public_tests

import (
	"testing"
)

func IsVegetarian(ingredients []string) bool {
	for _, ing := range ingredients {
		switch ing {
		case "Tuna", "Salmon":
			return false
		}
	}
	return true
}

func TestPublicIsVegetarianEdgeCases(t *testing.T) {
	cases := []struct {
		ingredients []string
		expected    bool
	}{
		{[]string{"Carrot", "Rice", "Nori"}, true},
		{[]string{"Ham", "Rice"}, true},
		{[]string{"Tuna", "Rice"}, false},
		{[]string{"Salmon", "Nori", "Rice"}, false},
	}
	for _, tc := range cases {
		isVeg := IsVegetarian(tc.ingredients)
		if isVeg != tc.expected {
			t.Errorf("IsVegetarian(%v) expected %v, got %v", tc.ingredients, tc.expected, isVeg)
		}
	}
}