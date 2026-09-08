package original

import (
	"testing"
	"reflect"
)

func testFooshiBar() *Restaurant {
	return &Restaurant{
		Name:     "Fooshi Bar",
		Location: "Buenos Aires",
		Menu:     []string{"Ebi Nigiri", "Edamame", "Inarizushi", "Kappa Maki", "Miso Soup", "Sake Nigiri", "Tamagoyaki"},
	}
}

func testRecipes() map[string][]string {
	return map[string][]string{
		"California Roll": {"Rice", "Cucumber", "Avocado", "Crab"},
		"Ebi Nigiri":      {"Shrimp", "Rice"},
		"Inarizushi":      {"Fried tofu", "Rice"},
		"Kappa Maki":      {"Cucumber", "Rice", "Nori"},
		"Maguro Nigiri":   {"Tuna", "Rice", "Nori"},
		"Sake Nigiri":     {"Salmon", "Rice", "Nori"},
		"Tamagoyaki":      {"Fried egg", "Rice", "Nori"},
		"Tsunamayo Maki":  {"Tuna", "Mayonnaise"},
	}
}

func TestFooshiBarFixture(t *testing.T) {
	fooshiBar := testFooshiBar()
	if fooshiBar.Name != "Fooshi Bar" {
		t.Errorf("Name mismatch: %s", fooshiBar.Name)
	}
	if fooshiBar.Location != "Buenos Aires" {
		t.Errorf("Location mismatch: %s", fooshiBar.Location)
	}
	if !sliceContains(fooshiBar.Menu, "Ebi Nigiri") {
		t.Errorf("Ebi Nigiri not in menu")
	}
	if !sliceContains(fooshiBar.Menu, "Tamagoyaki") {
		t.Errorf("Tamagoyaki not in menu")
	}
}

func TestRecipesFixture(t *testing.T) {
	recipes := testRecipes()
	if !reflect.DeepEqual(recipes["California Roll"], []string{"Rice", "Cucumber", "Avocado", "Crab"}) {
		t.Errorf("California Roll ingredients mismatch")
	}
	if _, ok := recipes["Ebi Nigiri"]; !ok {
		t.Errorf("Ebi Nigiri missing in recipes")
	}
}

func TestSushiFixtureParam(t *testing.T) {
	recipes := testRecipes()
	cases := []struct {
		sushiName string
	}{
		{"California Roll"},
		{"Ebi Nigiri"},
		{"Tamagoyaki"},
	}
	for _, tc := range cases {
		s, err := NewSushi(tc.sushiName, recipes[tc.sushiName])
		if err != nil {
			t.Errorf("unexpected error: %v", err)
		}
		if s.Name != tc.sushiName {
			t.Errorf("Wrong name for sushi, got %s", s.Name)
		}
		if len(s.Ingredients) == 0 {
			t.Errorf("Sushi ingredients are empty")
		}
	}
}

func sliceContains(list []string, v string) bool {
	for _, s := range list {
		if s == v {
			return true
		}
	}
	return false
}