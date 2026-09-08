package original

import (
	"reflect"
	"testing"
	"underscore"
)

func TestMap(t *testing.T) {
	result := underscore.Map([]int{1, 2, 3}, func(x int) int { return x * 2 })
	expected := []int{2, 4, 6}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}