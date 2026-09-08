package public_tests

import "testing"

func TestPublicMainTrue(t *testing.T) {
	if !boolFromSlice([]int{1}) {
		t.Errorf("bool value incorrect")
	}
}

func boolFromSlice(ints []int) bool {
	return len(ints) > 0
}

func TestPublicMainValue(t *testing.T) {
	val := "hamms"
	if _, ok := interface{}(val).(string); !ok {
		t.Errorf("'hamms' is expected to be a string")
	}
}