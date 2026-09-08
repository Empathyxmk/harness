package public_tests

import (
	"reflect"
	"testing"
)

func TestBasicAssertEq(t *testing.T) {
	if 2 != 2 {
		t.Fatalf("2 != 2")
	}
	if "bar" != "bar" {
		t.Fatalf(`"bar" != "bar"`)
	}
	if !reflect.DeepEqual([]int{5, 6}, []int{5, 6}) {
		t.Fatalf("slices not equal")
	}
}

func TestBasicAssertNe(t *testing.T) {
	if 3 == 4 {
		t.Fatalf("3 == 4")
	}
	if reflect.DeepEqual([]string{"x"}, []string{"y"}) {
		t.Fatalf("slices unexpectedly equal")
	}
}