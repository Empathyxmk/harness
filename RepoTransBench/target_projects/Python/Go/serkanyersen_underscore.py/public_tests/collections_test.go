package public_tests

import (
	"reflect"
	"testing"
	"underscore"
)

func TestMapPublic(t *testing.T) {
	result := underscore.Map([]int{4, 5, 6}, func(x int) int { return x + 1 })
	expected := []int{5, 6, 7}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}