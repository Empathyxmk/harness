package original

import (
	"testing"
)

func TestRestaurantEmptyMenuListRaises(t *testing.T) {
	_, err := NewRestaurant("Foo", "Bar", []string{})
	if err == nil {
		t.Fatalf("expected error for empty menu list")
	}
}

func TestSushiEmptyIngredientsListRaises(t *testing.T) {
	_, err := NewSushi("Foo", []string{})
	if err == nil {
		t.Fatalf("expected error for empty ingredients list")
	}
}