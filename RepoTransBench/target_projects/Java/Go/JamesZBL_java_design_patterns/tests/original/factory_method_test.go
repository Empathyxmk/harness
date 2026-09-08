package original

import (
	"testing"

	"jameszbl_java_design_patterns/factorymethod"
)

func TestFactoryMethodWesternHot(t *testing.T) {
	cook := factorymethod.NewWesternCook()
	food := cook.CookFood(factorymethod.FoodTypeHot)
	verifyFood(t, food, "WesternFood", factorymethod.FoodTypeHot)
}

func TestFactoryMethodWesternCold(t *testing.T) {
	cook := factorymethod.NewWesternCook()
	food := cook.CookFood(factorymethod.FoodTypeCold)
	verifyFood(t, food, "WesternFood", factorymethod.FoodTypeCold)
}

func TestFactoryMethodChineseHot(t *testing.T) {
	cook := factorymethod.NewChineseCook()
	food := cook.CookFood(factorymethod.FoodTypeHot)
	verifyFood(t, food, "ChineseFood", factorymethod.FoodTypeHot)
}

func TestFactoryMethodChineseCold(t *testing.T) {
	cook := factorymethod.NewChineseCook()
	food := cook.CookFood(factorymethod.FoodTypeCold)
	verifyFood(t, food, "ChineseFood", factorymethod.FoodTypeCold)
}

func verifyFood(t *testing.T, food factorymethod.Food, wantClass string, wantType factorymethod.FoodType) {
	if food.GetType() != wantType {
		t.Errorf("food type = %v, want %v", food.GetType(), wantType)
	}
	if !food.IsClass(wantClass) {
		t.Errorf("food class = %v, want subclass %v", food.GetClass(), wantClass)
	}
}