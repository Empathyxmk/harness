package original

import (
	"testing"
)

func TestFooshiServesVegetarianSushi(t *testing.T) {
	fooshiBar := testFooshiBar()
	vegetarianSushis := []string{"Kappa Maki", "Tamagoyaki", "Inarizushi"}
	sideDishes := []string{"Edamame", "Miso Soup"}
	for _, sushi := range vegetarianSushis {
		s, err := NewSushi(sushi, testRecipes()[sushi])
		if err != nil {
			t.Fatalf("unexpected sushi error: %v", err)
		}
		if !s.IsVegetarian() {
			t.Errorf("expected %s to be vegetarian", s.Name)
		}
		if !sliceContains(fooshiBar.Menu, s.Name) {
			t.Errorf("%s not in menu", s.Name)
		}
		for _, side := range sideDishes {
			if !sliceContains(fooshiBar.Menu, side) {
				t.Errorf("side dish %s not in menu", side)
			}
		}
	}
}

func TestSushiNonEmpty(t *testing.T) {
	s, err := NewSushi("Kappa Maki", []string{"Cucumber", "Rice", "Nori"})
	if err != nil {
		t.Fatalf("unexpected sushi error: %v", err)
	}
	if s.Name == "" {
		t.Errorf("Expected sushi name to be non-empty")
	}
	if len(s.Ingredients) == 0 {
		t.Errorf("Expected ingredients to be non-empty")
	}
}