package original

import (
	"testing"
)

func TestIsVegetarianWithAllNonveg(t *testing.T) {
	s, _ := NewSushi("Mix", []string{"Crab", "Salmon", "Shrimp", "Tuna", "Rice"})
	if s.IsVegetarian() {
		t.Errorf("expected non-vegetarian for all non-veg ingredients (proper-case)")
	}
}

func TestIsVegetarianWithMixedCase(t *testing.T) {
	s, _ := NewSushi("Strange", []string{"crab", "salmon", "shrimp", "tuna"})
	// Lowercase -- doesn't match non-veg proper-case, so vegetarian.
	if !s.IsVegetarian() {
		t.Errorf("expected vegetarian for all lower-case non-meat ingredients")
	}
}