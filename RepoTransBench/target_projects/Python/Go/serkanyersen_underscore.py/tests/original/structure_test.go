package original

import (
	"reflect"
	"testing"
	"underscore"
)

func TestPairs(t *testing.T) {
	result := underscore.Pairs(map[string]int{"a": 1, "b": 2})
	expected := [][2]interface{}{{"a", 1}, {"b", 2}}
	// Since pair order in maps is not guaranteed, we check elements
	var found int
	for _, exp := range expected {
		for _, got := range result {
			if reflect.DeepEqual(got, exp) {
				found++
				break
			}
		}
	}
	if found != len(expected) {
		t.Errorf("expected all pairs in result %v, got %v", expected, result)
	}
}