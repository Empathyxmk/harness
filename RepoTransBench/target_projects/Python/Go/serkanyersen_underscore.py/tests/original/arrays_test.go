package original

import (
	"reflect"
	"testing"
	"underscore"
)

func TestChunk(t *testing.T) {
	result := underscore.Chunk([]int{1, 2, 3, 4}, 2)
	expected := [][]int{{1, 2}, {3, 4}}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}

func TestCompact(t *testing.T) {
	// In Go, 0, false, "" are all varying types, so we use interface{}
	result := underscore.Compact([]interface{}{0, 1, false, 2, "", 3})
	expected := []interface{}{1, 2, 3}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}