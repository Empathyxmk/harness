package public_tests

import (
	"reflect"
	"testing"
	"underscore"
)

func TestChunkPublic(t *testing.T) {
	result := underscore.Chunk([]int{10, 20, 30, 40, 50}, 3)
	expected := [][]int{{10, 20, 30}, {40, 50}}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}

func TestCompactPublic(t *testing.T) {
	result := underscore.Compact([]interface{}{nil, "hello", "", 0, 9, false, 5})
	expected := []interface{}{"hello", 9, 5}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}