package public_tests

import (
	"testing"
)

type SushiU struct {
	Name        string
	Ingredients []string
}

func (s *SushiU) Contains(ingredient string) bool {
	for _, ing := range s.Ingredients {
		if ing == ingredient {
			return true
		}
	}
	return false
}
func (s *SushiU) IsVegetarian() bool {
	for _, ing := range s.Ingredients {
		switch ing {
		case "Tuna", "Shrimp":
			return false
		}
	}
	return true
}
type RestaurantU struct {
	Name string
	Menu []string
}
func NewSushiU(name string, ingredients []string) (*SushiU, error) {
	if ingredients == nil {
		return nil, errNoIngredients
	}
	return &SushiU{Name: name, Ingredients: ingredients}, nil
}
func NewRestaurantU(name string, menu []string) (*RestaurantU, error) {
	if menu == nil {
		return nil, errNoMenu
	}
	return &RestaurantU{Name: name, Menu: menu}, nil
}
var errNoIngredients = errorString("no ingredients")
var errNoMenu = errorString("no menu")
type errorString string
func (e errorString) Error() string { return string(e) }

func TestInitRaisesValueErrorIfIngredientsIsNull(t *testing.T) {
	_, err := NewSushiU("California Roll", nil)
	if err == nil {
		t.Errorf("expected error for nil ingredients")
	}
}
func TestInitRaisesValueErrorIfMenuIsNull(t *testing.T) {
	_, err := NewRestaurantU("Sushiland", nil)
	if err == nil {
		t.Errorf("expected error for nil menu")
	}
}
func TestInitWorksWithValidData(t *testing.T) {
	r, err := NewRestaurantU("Sushiland", []string{"Kani Nigiri"})
	if err != nil {
		t.Fatalf("unexpected: %v", err)
	}
	if r.Menu[0] != "Kani Nigiri" {
		t.Errorf("menu mismatch")
	}
	s, err := NewSushiU("Kani Nigiri", []string{"Crab", "Rice"})
	if err != nil {
		t.Fatalf("unexpected: %v", err)
	}
	if s.Name != "Kani Nigiri" {
		t.Errorf("sushi name mismatch")
	}
	if !s.Contains("Crab") {
		t.Errorf("expected Crab in sushi")
	}
}
func TestContainsOperatorFalse(t *testing.T) {
	s := &SushiU{"Avocado Roll", []string{"Avocado", "Rice", "Nori"}}
	if s.Contains("Cucumber") {
		t.Errorf("did not expect cucumber in Avocado Roll")
	}
}
func TestContainsOperatorTrue(t *testing.T) {
	s := &SushiU{"Avocado Roll", []string{"Avocado", "Rice", "Nori"}}
	if !s.Contains("Avocado") {
		t.Errorf("expected avocado in Avocado Roll")
	}
}
func TestIsVegetarianProperty(t *testing.T) {
	cases := []struct {
		ingredients []string
		isVeg       bool
	}{
		{[]string{"Avocado", "Rice", "Nori"}, true},
		{[]string{"Tuna", "Rice", "Nori"}, false},
		{[]string{"Egg", "Rice"}, true},
		{[]string{"Shrimp", "Rice"}, false},
	}
	for _, tc := range cases {
		s := &SushiU{"Custom Roll", tc.ingredients}
		if s.IsVegetarian() != tc.isVeg {
			t.Errorf("IsVegetarian(%v) expected %v, got %v", tc.ingredients, tc.isVeg, s.IsVegetarian())
		}
	}
}