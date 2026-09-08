package original

import (
	"reflect"
	"testing"
)

type Restaurant struct {
	Name     string
	Location string
	Menu     []string
}

func NewRestaurant(name, location string, menu []string) (*Restaurant, error) {
	if menu == nil || len(menu) == 0 {
		return nil, ErrNoMenu
	}
	return &Restaurant{Name: name, Location: location, Menu: menu}, nil
}

type Sushi struct {
	Name        string
	Ingredients []string
}

func NewSushi(name string, ingredients []string) (*Sushi, error) {
	if ingredients == nil || len(ingredients) == 0 {
		return nil, ErrNoIngredients
	}
	return &Sushi{Name: name, Ingredients: ingredients}, nil
}

func (s *Sushi) Contains(ingredient string) bool {
	for _, ing := range s.Ingredients {
		if ing == ingredient {
			return true
		}
	}
	return false
}

func (s *Sushi) IsVegetarian() bool {
	for _, ing := range s.Ingredients {
		switch ing {
		case "Crab", "Salmon", "Shrimp", "Tuna":
			return false
		}
	}
	return true
}

var ErrNoMenu = &customError{"no menu provided"}
var ErrNoIngredients = &customError{"no ingredients provided"}

type customError struct{ s string }
func (e *customError) Error() string { return e.s }

func TestRestaurantInitValid(t *testing.T) {
	rest, err := NewRestaurant("Foo", "Bar", []string{"Sushi1", "Sushi2"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if rest.Name != "Foo" {
		t.Errorf("expected name Foo, got %v", rest.Name)
	}
	if rest.Location != "Bar" {
		t.Errorf("expected location Bar, got %v", rest.Location)
	}
	if !reflect.DeepEqual(rest.Menu, []string{"Sushi1", "Sushi2"}) {
		t.Errorf("expected menu Sushi1,Sushi2, got %v", rest.Menu)
	}
}

func TestRestaurantInitNoMenuRaises(t *testing.T) {
	_, err := NewRestaurant("NoMenu", "Where", nil)
	if err == nil {
		t.Fatalf("expected error for no menu")
	}
	_, err = NewRestaurant("NoMenu", "Where", []string{})
	if err == nil {
		t.Fatalf("expected error for empty menu")
	}
}

func TestSushiInitValid(t *testing.T) {
	s, err := NewSushi("Veggie", []string{"Cucumber", "Rice"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if s.Name != "Veggie" {
		t.Errorf("expected name Veggie, got %v", s.Name)
	}
	if !reflect.DeepEqual(s.Ingredients, []string{"Cucumber", "Rice"}) {
		t.Errorf("unexpected ingredients: %v", s.Ingredients)
	}
}

func TestSushiInitNoIngredientsRaises(t *testing.T) {
	_, err := NewSushi("Nothing", nil)
	if err == nil {
		t.Fatalf("expected error for nil ingredients")
	}
	_, err = NewSushi("Nothing", []string{})
	if err == nil {
		t.Fatalf("expected error for empty ingredients")
	}
}

func TestSushiContainsTrue(t *testing.T) {
	s, _ := NewSushi("Veggie", []string{"Cucumber", "Rice"})
	if !s.Contains("Cucumber") {
		t.Errorf("expected true for containment")
	}
}

func TestSushiContainsFalse(t *testing.T) {
	s, _ := NewSushi("Veggie", []string{"Cucumber", "Rice"})
	if s.Contains("Avocado") {
		t.Errorf("expected false for non-containment")
	}
}

func TestSushiIsVegetarian(t *testing.T) {
	cases := []struct {
		ingredients []string
		expected    bool
	}{
		{[]string{"Rice", "Cucumber"}, true},
		{[]string{"Rice", "Crab"}, false},
		{[]string{"Salmon", "Rice"}, false},
		{[]string{"Shrimp", "Rice"}, false},
		{[]string{"Tuna", "Rice"}, false},
		{[]string{"Egg", "Nori"}, true},
	}
	for _, tc := range cases {
		s, _ := NewSushi("Test", tc.ingredients)
		if s.IsVegetarian() != tc.expected {
			t.Errorf("IsVegetarian(%v) expected %v, got %v", tc.ingredients, tc.expected, s.IsVegetarian())
		}
	}
}