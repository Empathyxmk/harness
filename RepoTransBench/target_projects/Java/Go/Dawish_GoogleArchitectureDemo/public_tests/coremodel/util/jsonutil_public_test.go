package util

import (
	"encoding/json"
	"strings"
	"testing"
)

type Animal struct {
	Type string `json:"type"`
	Age  int    `json:"age"`
}

func (a Animal) Equals(b Animal) bool {
	return a.Type == b.Type && a.Age == b.Age
}

func TestStr2JsonBeanWithDifferentData(t *testing.T) {
	animalJson := `{"type":"Dog","age":4}`
	var animal Animal
	err := json.Unmarshal([]byte(animalJson), &animal)
	if err != nil {
		t.Fatalf("json.Unmarshal failed: %v", err)
	}
	if animal.Type != "Dog" {
		t.Errorf("expected type Dog, got %s", animal.Type)
	}
	if animal.Age != 4 {
		t.Errorf("expected age 4, got %d", animal.Age)
	}
}

func TestJsonBean2StrWithDifferentData(t *testing.T) {
	animal := Animal{"Cat", 2}
	jsonBytes, err := json.Marshal(animal)
	if err != nil {
		t.Fatalf("json.Marshal failed: %v", err)
	}
	jsonStr := string(jsonBytes)
	if !strings.Contains(jsonStr, `"type":"Cat"`) && !strings.Contains(jsonStr, `"type": "Cat"`) {
		t.Errorf(`expected json to contain '"type":"Cat"', got %s`, jsonStr)
	}
	if !strings.Contains(jsonStr, `"age":2`) && !strings.Contains(jsonStr, `"age": 2"`) {
		t.Errorf(`expected json to contain '"age":2', got %s`, jsonStr)
	}
}

func TestJsonList2StrWithDifferentData(t *testing.T) {
	animalList := []Animal{
		{"Horse", 7},
		{"Rabbit", 1},
	}
	jsonBytes, err := json.Marshal(animalList)
	if err != nil {
		t.Fatalf("json.Marshal list failed: %v", err)
	}
	jsonStr := string(jsonBytes)
	if !strings.HasPrefix(jsonStr, "[") || !strings.HasSuffix(jsonStr, "]") {
		t.Errorf("expected result to be a JSON array: %s", jsonStr)
	}
	if !strings.Contains(jsonStr, `"type":"Horse"`) && !strings.Contains(jsonStr, `"type": "Horse"`) {
		t.Error("missing 'type:Horse'")
	}
	if !strings.Contains(jsonStr, `"type":"Rabbit"`) && !strings.Contains(jsonStr, `"type": "Rabbit"`) {
		t.Error("missing 'type:Rabbit'")
	}
}