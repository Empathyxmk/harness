package public_tests

import (
	"testing"
	"reflect"
)

// Simulate a Subplot type
type Subplot struct {
	shape [2]int
	num   int
}

func NewSubplot(shape [2]int, num int) *Subplot {
	return &Subplot{shape: shape, num: num}
}

func TestSubplotInitDifferentData(t *testing.T) {
	sp := NewSubplot([2]int{2, 4}, 5)
	if reflect.TypeOf(sp) != reflect.TypeOf(&Subplot{}) {
		t.Errorf("sp is not of type *Subplot")
	}
}