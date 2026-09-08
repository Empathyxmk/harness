package tests

import (
	"testing"
	"reflect"
)

// Simulate a Subplot class as the Python test looks for any class
type Subplot struct {
	shape [2]int
	num   int
}

func NewSubplot(shape [2]int, num int) *Subplot {
	return &Subplot{shape: shape, num: num}
}

func TestSubplotInit(t *testing.T) {
	sp := NewSubplot([2]int{3, 3}, 7)
	if reflect.TypeOf(sp) != reflect.TypeOf(&Subplot{}) {
		t.Errorf("sp is not of type *Subplot")
	}
}