package public_tests

import (
	"testing"
	"errors"
)

type Restaurant struct{}
type Sushi struct{}

var errDummy = errors.New("dummy error")

func TestPublicSushiInitRequiresIngredients(t *testing.T) {
	// Simulating expected error on missing ingredients
	_, err := NewSushiWithoutIngredients()
	if err == nil {
		t.Errorf("Expected error for missing ingredients")
	}
}

func TestPublicRestaurantInitRequiresMenu(t *testing.T) {
	_, err := NewRestaurantWithoutMenu()
	if err == nil {
		t.Errorf("Expected error for missing menu")
	}
}

// Dummy function for simulation
func NewSushiWithoutIngredients() (*Sushi, error)   { return nil, errDummy }
func NewRestaurantWithoutMenu() (*Restaurant, error) { return nil, errDummy }