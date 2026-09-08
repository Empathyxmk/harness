package public_tests

import (
	"reflect"
	"testing"
	"underscore"
)

func TestPairsPublic(t *testing.T) {
	result := underscore.Pairs(map[string]int{"foo": 7, "bar": 8})
	// Expected: [("foo", 7), ("bar", 8)]
	expected := [][2]interface{}{{"foo", 7}, {"bar", 8}}
	found := 0
	for _, exp := range expected {
		for _, got := range result {
			if reflect.DeepEqual(got, exp) {
				found++
			}
		}
	}
	if found != len(expected) {
		t.Errorf("expected all pairs %v in result %v", expected, result)
	}
}