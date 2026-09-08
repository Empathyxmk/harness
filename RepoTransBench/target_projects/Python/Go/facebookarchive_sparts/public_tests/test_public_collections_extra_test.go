package public_tests

import (
	"reflect"
	"sort"
	"testing"
)

func TestPublicCollectionsExtraDummy(t *testing.T) {
	lst := []int{10, 2, 7, 4, 2}
	s := make(map[int]struct{})
	for _, v := range lst {
		s[v] = struct{}{}
	}
	if len(s) != 4 {
		t.Errorf("expected 4 unique elements, got %d", len(s))
	}
	var vals []int
	for k := range s {
		vals = append(vals, k)
	}
	sort.Ints(vals)
	expected := []int{2, 4, 7, 10}
	if !reflect.DeepEqual(vals, expected) {
		t.Errorf("expected sorted set %v, got %v", expected, vals)
	}
}